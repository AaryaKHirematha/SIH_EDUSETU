import pickle
import struct
import io
import re

p = "model_cache/pytorch_model.bin"

class FakeStorage:
    def __init__(self, pid):
        self.pid = pid

class U(pickle.Unpickler):
    def persistent_load(self, pid):
        return FakeStorage(pid)

    def find_class(self, module, name):
        if module == "torch._utils" and name in (
            "_rebuild_tensor_v2",
            "_rebuild_tensor",
        ):
            def rebuild(storage, storage_offset, size, stride, *args):
                return {
                    "size": tuple(size),
                    "stride": tuple(stride),
                }
            return rebuild

        return super().find_class(module, name)

with open(p, "rb") as f:
    header = f.read(30)

    name_len = struct.unpack("<H", header[26:28])[0]
    extra_len = struct.unpack("<H", header[28:30])[0]

    name = f.read(name_len)
    f.read(extra_len)

    print("Archive:", name.decode())
    print("Pickle offset:", f.tell())

    # Read metadata only.
    # Do NOT load the 3.6 GB tensor storage.
    data = f.read(2 * 1024 * 1024)

obj = U(io.BytesIO(data)).load()
keys = list(obj.keys())

print()
print("=" * 60)
print("LOCAL CHECKPOINT ARCHITECTURE")
print("=" * 60)

print("Tensor entries:", len(keys))

encoder_layers = []
decoder_layers = []

for k in keys:
    m = re.search(r"encoder\.layers\.(\d+)", k)
    if m:
        encoder_layers.append(int(m.group(1)))

    m = re.search(r"decoder\.layers\.(\d+)", k)
    if m:
        decoder_layers.append(int(m.group(1)))

print("Encoder layers:", max(encoder_layers) + 1)
print("Decoder layers:", max(decoder_layers) + 1)

print()
print("KEY TENSOR SHAPES")
print("-" * 60)

for k in [
    "model.shared.weight",
    "model.encoder.embed_tokens.weight",
    "model.decoder.embed_tokens.weight",
    "lm_head.weight",
]:
    if k in obj:
        print(f"{k:40} {obj[k]['size']}")

print()
print("LAYER DIMENSIONS")
print("-" * 60)

for k in keys:
    if k.endswith("self_attn.q_proj.weight"):
        print("Attention Q:", obj[k]["size"])
        break

for k in keys:
    if k.endswith("fc1.weight"):
        print("FFN:", obj[k]["size"])
        break

print()
print("No model weights were loaded into RAM.")
