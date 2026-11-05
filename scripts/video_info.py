import struct
from pathlib import Path
path=Path(__file__).resolve().parents[1]/'public/demo.mp4'
data=path.read_bytes()
offset=data.index(b'mvhd')+4
version=data[offset]
if version==0:
    scale,duration=struct.unpack_from('>II',data,offset+12)
else:
    scale=struct.unpack_from('>I',data,offset+20)[0]
    duration=struct.unpack_from('>Q',data,offset+24)[0]
seconds=duration/scale
assert 60<=seconds<=90,seconds
print(f'MP4 gerçek süresi: {seconds:.3f} saniye; {len(data)} bayt.')
