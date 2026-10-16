# Verzia na FTP: obrázky a videá, ktoré už sú na FTP (galeria/, vylety/, videa/, ostatne/), sa načítajú ako súbory
import sys, re, base64, hashlib, glob, os
src, root, out = sys.argv[1:4]
H = {hashlib.md5(open(f, 'rb').read()).hexdigest(): os.path.relpath(f, root) for f in glob.glob(root + '/*/*')}
s = open(src).read(); n = 0
def rep(m):
    global n
    h = hashlib.md5(base64.b64decode(m.group(2))).hexdigest()
    if h in H: n += 1; return H[h]
    return m.group(0)
s = re.sub(r'data:([a-z]+/[a-z0-9.+-]+);base64,([A-Za-z0-9+/=]{3000,})', rep, s)
open(out, 'w').write(s)
print('nahradených', n, 'súborov; HTML', os.path.getsize(out) // 1024, 'KB')
