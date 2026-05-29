# Release Runbook

Luban Loop supports two install channels:

- Stable: installs the latest tagged release by default.
- Development: install from `main` only when explicitly requested.

## Stable Install

Use the one-line installer. It resolves GitHub's latest release tag automatically:

```bash
curl -fsSL https://raw.githubusercontent.com/Zanetach/luban-loop/main/scripts/install.sh | bash
```

For release verification or reproducible installs, pin the tag recorded in `VERSION`:

```bash
curl -fsSL https://raw.githubusercontent.com/Zanetach/luban-loop/main/scripts/install.sh | LUBAN_LOOP_REF="v$(cat VERSION)" bash
```

The `LUBAN_LOOP_REF` environment variable is optional. When omitted, the installer downloads the latest tagged release archive before installing the skill bundle.

## Development Install

Use this only when intentionally tracking active development:

```bash
curl -fsSL https://raw.githubusercontent.com/Zanetach/luban-loop/main/scripts/install.sh | LUBAN_LOOP_REF=main bash
```

## Local Checkout Install

If the repository is already cloned, install directly from local files:

```bash
./scripts/install.sh
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
