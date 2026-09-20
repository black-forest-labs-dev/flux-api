        """Minimal FLUX (Black Forest Labs) example: create one prediction and print the output URL(s)."""
        import flux_api

        output = flux_api.run({
    "prompt": "A cinematic shot of a lighthouse at dawn, soft fog, warm light"
})
        print(output)
