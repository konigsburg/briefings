import json,base64,urllib.request,urllib.error,os
TOK=os.environ.get("GH_PUB_TOKEN") or (open("/home/claude/.ghtoken").read().strip() if os.path.exists("/home/claude/.ghtoken") else "")
OWNER,REPO="konigsburg","briefings"
TARGET=os.environ.get("PUB_TARGET","data/today.json")
MODE=os.environ.get("PUB_MODE","merge")
op=urllib.request.build_opener(urllib.request.ProxyHandler({}))
def api(m,p,b=None):
    r=urllib.request.Request(f"https://api.github.com{p}",data=(json.dumps(b).encode() if b else None),method=m)
    for k,v in {"Authorization":"Bearer "+TOK,"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"}.items():r.add_header(k,v)
    try:
        x=op.open(r,timeout=60);raw=x.read().decode();return x.status,(json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        raw=e.read().decode()
        try:return e.code,json.loads(raw)
        except:return e.code,{"raw":raw}
def getjson(path):
    sc,cur=api("GET",f"/repos/{OWNER}/{REPO}/contents/{path}")
    if sc==200 and cur.get("content"):
        try:return json.loads(base64.b64decode(cur["content"])),cur.get("sha")
        except:return None,cur.get("sha")
    return None,None
def putjson(path,obj,msg,sha):
    body={"message":msg,"content":base64.b64encode(json.dumps(obj,ensure_ascii=False,indent=2).encode()).decode(),"branch":"main"}
    if sha:body["sha"]=sha
    return api("PUT",f"/repos/{OWNER}/{REPO}/contents/{path}",body)[0]
payload=json.load(open("/tmp/payload.json"))
cur,sha=getjson(TARGET)
obj=payload if MODE=="replace" else {**(cur or {}), **payload}
print("target",TARGET,putjson(TARGET,obj,"Update "+TARGET,sha))
if os.path.exists("/tmp/arch.json"):
    entry=json.load(open("/tmp/arch.json"))
    arch,ash=getjson("data/archive.json"); arch=arch or []
    arch=[e for e in arch if e.get("id")!=entry.get("id")]
    arch.insert(0,entry); arch=arch[:30]
    print("archive",putjson("data/archive.json",arch,"Archive "+entry.get("kind",""),ash))
