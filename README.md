# cloud-haven-consultants

The Cloud Haven Consultants website includes the service directory, editorial guides, interactive Three.js globe and consultation brief builder.

## Run locally

From the repository root, run:

```sh
python3 src/build.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000/. The static generator uses the Python standard library. Fonts, photographs and the globe are served from `dist/assets`.

## Deploy

Import this repository into Vercel with the repository root as the project directory. `vercel.json` sets the build command and output directory. The build uses Vercel’s production domain for canonical links and the sitemap. Set `SITE_URL` to an absolute HTTPS URL to use a custom domain.
