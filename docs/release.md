# Release Runbook

Luban Loop supports two install channels:

- Stable: install from a tagged release.
- Latest: install from `main` for active development.

## Stable Install

Use the tag recorded in `VERSION`:

```bash
VERSION_TAG="v$(cat VERSION)"
curl -fsSL "https://raw.githubusercontent.com/Zanetach/luban-loop/${VERSION_TAG}/scripts/install.sh" | LUBAN_LOOP_REF="${VERSION_TAG}" bash
```

The `LUBAN_LOOP_REF` environment variable is required because the installer downloads the repository archive before installing the skill bundle.

## Latest Install

Use this only when intentionally tracking active development:

```bash
curl -fsSL https://raw.githubusercontent.com/Zanetach/luban-loop/main/scripts/install.sh | bash
```

## Release Checklist

1. Update `VERSION`.
2. Run `./scripts/verify.sh`.
3. Commit the release changes.
4. Create and push the tag:

```bash
VERSION_TAG="v$(cat VERSION)"
git tag -a "${VERSION_TAG}" -m "Release ${VERSION_TAG}"
git push origin main "${VERSION_TAG}"
```

5. Confirm GitHub Actions `Verify` passes for the pushed tag or commit.
6. Use the stable install command above to smoke-test the tagged installer.

Do not create a release tag from a dirty worktree.
