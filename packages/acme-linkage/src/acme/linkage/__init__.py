from acme.db import upload


def link_and_upload(left: list[dict], right: list[dict], key: str) -> None:
    index = {r[key]: r for r in right}
    linked = [{**l, **index[l[key]]} for l in left if l[key] in index]
    upload(linked, "linked")
