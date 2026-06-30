# Extraction Rules

## Center Event Is the Unit

Extract one hyperedge for one essential event or claim. A hyperedge is not a paragraph summary and not a list of every interesting fact.

Accept a candidate node only when it:

- Is an argument of the main trigger.
- Modifies the main event's time, place, cause, purpose, or method.
- Describes the main system, capability, quantity, platform, actor, target, or claim.

Reject a candidate when it:

- Describes a neighboring event.
- Is background or future context not needed for the main event.
- Is a consequence when the slot asks for cause.
- Is an attractive technical detail but not part of the main event frame.

## Batch Splitting

Use multiple hyperedges only when pasted text contains independent snippets.

Strong split signals:

- Paragraph starts with a new country, company, person, or institution and a new main predicate.
- Source or topic changes sharply.
- Time and place reset and no previous actor or object carries over.
- Each paragraph could stand alone as a separate news brief.

Weak signals that should not split by themselves:

- Additional quantities.
- Technical specifications.
- Platform examples.
- Historical background.
- Follow-up comments from the same actor.

## Military News Node Types

- `who`: country, ministry, company, military service, commander, platform, unit, source.
- `what`: weapon system, platform, quantity, capability, test, deployment, construction, disclosure, claim.
- `when`: publication date, cutoff date, exercise or test date, deadline, planned completion date.
- `where`: theater, base, sea area, airspace, exhibition venue, platform, city, country.
- `why`: threat, deterrence, operational need, mission goal, policy reason, stated purpose.
- `how`: simulation, test profile, carrier platform, guidance method, fire-control system, installation method, deployment method.

## Why vs How

- `why`: for what reason or purpose.
- `how`: by what method, mechanism, tool, or platform.

Examples:

- A phrase meaning "use computer modeling" -> how/method.
- A phrase meaning "weaken nuclear deterrence" -> why/threat if it motivates the action.
- A phrase meaning "mounted on the rear of a 4x4 chassis" -> how/platform.
- A phrase meaning "to improve autonomy and endurance" -> why/purpose.

## Attribution Handling

If the center event is a reported fact, keep the reporting organization as `source`, not as the main actor.

If the center event is an announcement, statement, disclosure, or briefing, the announcing source can be the main `who`.

## Inventory Handling

For counts and equipment lists:

- Treat the disclosure, possession state, deployment status, or inventory summary as one center event.
- Merge many counts into 1-4 high-value `what` slots.
- Prefer grouped summaries such as `ICBM inventory`, `SLBM inventory`, and `bomber inventory`.
- Do not create separate events for every model, launcher, spare device, or test platform unless the user asks for exhaustive extraction.

## Capability Handling

For `can`, `able to`, `main advantage`, `designed to`, and similar phrases:

- Put the capability itself in `what`.
- Put the purpose or operational value in `why`.
- Put the technical mechanism, platform, or process in `how`.
- Do not turn every capability sentence into a separate event.

## Hypergraph Projection

Use 5W1H node groups as indexed arguments of one event hyperedge.

Default hyperedge:

```text
HE = predicate(event, who_nodes*, what_nodes*, when_nodes*, where_nodes*, why_nodes*, how_nodes*)
```

Do not build full graph nodes, RDF, triples, or Neo4j imports unless requested.
