# `$fpf` Help — Skills Development

Use this area for skill triggers and scope, prompt contracts, graph composition, tools and context connectors, evaluation cases, installation and portability, and quality, regression, or release.

## Typical profiles

- Skill trigger and scope
- Skill prompt contract
- Skill graph and composition
- Skill tools and context connector
- Skill evaluation cases
- Skill installation, portability, and runtime
- Skill quality, regression, and release

## Typical calls

- `$fpf problem frame Frame the skill task family, trigger, exclusions, and fallback.`
- `$fpf structure recover Recover the current prompt graph and tool dependencies.`
- `$fpf options explore Compare alternative skill compositions without choosing one.`
- `$fpf evaluation design Define routing, golden, counterexample, and regression cases.`
- `$fpf design challenge Challenge this proposed skill or connector before implementation.`
- `$fpf quality improve Improve the versioned skill and rerun its frozen cases.`
- `$fpf alignment audit Audit the installed skill runtime and release evidence.`

Use a composition only when each later node consumes an explicit earlier result. A changed prompt, rerun test, or new report does not by itself authorize another full review loop.
