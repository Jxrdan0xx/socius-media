#!/usr/bin/env python3
"""Schedule a post in Buffer (GraphQL API). The API key is NEVER stored in this repo:
it must be passed in the BUFFER_API_KEY environment variable (it lives only in the
private scheduled-task prompt).

Examples
  # LinkedIn document carousel on the Socius company page
  BUFFER_API_KEY=... python3 engine/buffer_post.py create --channel socius_li \
      --text-file post.txt --due "2026-11-05 12:15" \
      --document <pdf_url> --doc-title "Title" --thumb <cover_jpg_url>

  # Jordan's personal LinkedIn with an image and a linked @Socius tag
  ... create --channel jordan_li --text-file post.txt --due "2026-11-06 13:30" \
      --image <png_url> --mention-socius

  # Jordan's personal X: main post + replies (reply texts in files, link only in the last)
  ... create --channel jordan_x --text-file x1.txt --reply-file x2.txt --due "2026-11-06 16:45" --image <png_url>

  ... list --channel jordan_li        # scheduled posts on a channel
  ... delete --id <post_id>
"""
import argparse, json, os, sys, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

API = "https://api.buffer.com"
ORG = "6aeae05bbc5e44aae22f8da8"
CHANNELS = {
    "socius_li": "6aeafb78e29c69a1715a761d",  # Socius LinkedIn company page
    "jordan_li": "6aeafb78e29c69a1715a761c",  # Jordan Edwards personal LinkedIn
    "jordan_x": "6aeafc4de29c69a1715a7cba",   # @jxrdan0x personal X
}
SOCIUS_ORG = {
    "id": "106846565",
    "entity": "urn:li:organization:106846565",
    "link": "https://www.linkedin.com/company/sociustalent",
    "localizedName": "Socius",
    "vanityName": "sociustalent",
}


def gql(query, variables=None):
    key = os.environ.get("BUFFER_API_KEY")
    if not key:
        sys.exit("BUFFER_API_KEY is not set")
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        "User-Agent": "socius-media/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.load(r)
    if out.get("errors"):
        sys.exit("Buffer error: " + json.dumps(out["errors"])[:1500])
    return out["data"]


def utf16_index(text, idx):
    return len(text[:idx].encode("utf-16-le")) // 2


def london_to_utc(s):
    dt = datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo("Europe/London"))
    if dt <= datetime.now(ZoneInfo("Europe/London")):
        sys.exit("Refusing to schedule in the past: " + s)
    return dt.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def image_assets(urls):
    return [{"image": {"url": u, "thumbnailUrl": u}} for u in urls or []]


def create(a):
    text = open(a.text_file, encoding="utf-8").read().strip()
    channel = CHANNELS[a.channel]
    inp = {"channelId": channel, "text": text, "schedulingType": "automatic",
           "needsApproval": False, "assets": []}
    if a.draft:
        inp["saveToDraft"] = True
        inp["mode"] = "addToQueue"
    else:
        inp["mode"] = "customScheduled"
        inp["dueAt"] = london_to_utc(a.due)
    if a.document:
        inp["assets"] = [{"document": {"url": a.document, "title": a.doc_title or "Socius Talent",
                                        "thumbnailUrl": a.thumb}}]
    else:
        inp["assets"] = image_assets(a.image)
    meta = {}
    if a.mention_socius:
        if a.channel == "jordan_x":
            sys.exit("--mention-socius is LinkedIn only")
        # The post must contain the plain word 'Socius' (no @) where the tag should go.
        # The LAST occurrence is tagged (the sign-off line).
        i = text.rfind("Socius")
        if i < 0:
            sys.exit("Text has no 'Socius' to tag")
        ann = dict(SOCIUS_ORG, start=utf16_index(text, i), length=6)
        meta["linkedin"] = {"annotations": [ann]}
    if a.reply_file:
        if a.channel != "jordan_x":
            sys.exit("--reply-file is for X only")
        thread = [{"text": text, "assets": inp["assets"]}]
        for f in a.reply_file:
            thread.append({"text": open(f, encoding="utf-8").read().strip(), "assets": []})
        meta["twitter"] = {"thread": thread}
    if meta:
        inp["metadata"] = meta
    q = """mutation($input: CreatePostInput!){ createPost(input:$input){ __typename
      ... on PostActionSuccess { post { id status dueAt } }
      ... on InvalidInputError { message } ... on LimitReachedError { message }
      ... on UnexpectedError { message } ... on RestProxyError { message } } }"""
    try:
        res = gql(q, {"input": inp})["createPost"]
    except SystemExit as e:
        # Some error types may not exist in the schema; retry with only the known one.
        if "Unknown type" in str(e):
            q = """mutation($input: CreatePostInput!){ createPost(input:$input){ __typename
              ... on PostActionSuccess { post { id status dueAt } } ... on InvalidInputError { message } } }"""
            res = gql(q, {"input": inp})["createPost"]
        else:
            raise
    print(json.dumps(res))
    if res.get("__typename") != "PostActionSuccess":
        sys.exit(1)


def list_posts(a):
    q = """query($input: PostsInput!){ posts(input:$input){ edges { node { id status dueAt text channelId } } } }"""
    inp = {"organizationId": ORG, "filter": {"channelIds": [CHANNELS[a.channel]], "status": ["scheduled"]}}
    d = gql(q, {"input": inp})
    for e in d["posts"]["edges"]:
        n = e["node"]
        print(n["id"], n["status"], n["dueAt"], "|", (n["text"] or "")[:80].replace("\n", " "))


def delete(a):
    q = """mutation($input: DeletePostInput!){ deletePost(input:$input){ __typename } }"""
    print(json.dumps(gql(q, {"input": {"id": a.id}})))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="cmd", required=True)
    c = s.add_parser("create")
    c.add_argument("--channel", required=True, choices=CHANNELS)
    c.add_argument("--text-file", required=True)
    c.add_argument("--due", help="Europe/London 'YYYY-MM-DD HH:MM'")
    c.add_argument("--image", action="append", help="public image URL (repeatable)")
    c.add_argument("--document", help="public PDF URL (LinkedIn document carousel)")
    c.add_argument("--doc-title")
    c.add_argument("--thumb", help="cover image URL for the document")
    c.add_argument("--mention-socius", action="store_true")
    c.add_argument("--reply-file", action="append", help="X reply text file (repeatable)")
    c.add_argument("--draft", action="store_true", help="save as Buffer draft instead of scheduling")
    l = s.add_parser("list"); l.add_argument("--channel", required=True, choices=CHANNELS)
    d = s.add_parser("delete"); d.add_argument("--id", required=True)
    a = p.parse_args()
    if a.cmd == "create" and not a.draft and not a.due:
        sys.exit("--due is required unless --draft")
    {"create": create, "list": list_posts, "delete": delete}[a.cmd](a)
