"""The same client drives every hosted model listed in flux_api.MODELS."""
from flux_api import Client, MODELS

client = Client()
for slug, info in MODELS.items():
    print(slug, "->", info["category"], "required:", info["required"])
# pick one explicitly
output = client.run({"prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light"}, model="black-forest-labs/flux-1.1-pro")
print(output)
