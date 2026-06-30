# Trigger/Action Micro-Skill Library

Use these micro-skills after the center event is selected. Apply a skill only when its trigger is explicit in the source text.

In normal output, do not add an applied-skill log. If the user asks for debugging or method analysis, list applied micro-skills outside the JSON.

## MS01 Inventory Disclosure

Trigger:

- Phrases meaning disclose, release details, according to official details, as of a cutoff date, possess, deploy, reserve.
- Long lists of weapon counts, platforms, launchers, or inventories.

Action:

- Center event type: `disclosure` or `capability`.
- Predicate: `disclose` or `hold`.
- `who`: source if the act is disclosure; country or military owner if the act is possession/deployment status.
- `what`: group quantities into inventory categories.
- `when`: publication date and cutoff date.
- `where`: usually empty unless deployment locations are stated.
- Discard individual launchers, spare devices, and test platforms unless central.

## MS02 Risk Demonstration

Trigger:

- Phrases meaning use a method to demonstrate risk, show harm, show how something threatens security, weaken deterrence.

Action:

- Center event type: `risk_demonstration`.
- Predicate: `demonstrate`.
- `who`: demonstrating actor and target or threat actor.
- `what`: risk or harm claim.
- `why`: threat, deterrence concern, security concern.
- `how`: modeling, simulation, briefing, demonstration method.

## MS03 Exhibition Capability

Trigger:

- Phrases meaning exhibit, show, debut, air show, defense exhibition, display a weapon platform.

Action:

- Center event type: `exhibition`.
- Predicate: `exhibit`.
- `who`: exhibitor or manufacturer.
- `what`: exhibited system and primary capability.
- `when`: exhibition date.
- `where`: exhibition venue.
- `why`: operational purpose or advertised advantage if explicit.
- `how`: mounted platform, fire-control system, technical mechanism.

## MS04 Operational Test

Trigger:

- Phrases meaning complete operational test, evaluation, trial, flight profile, initial operational capability.

Action:

- Center event type: `test`.
- Predicate: `test` or `complete_test`.
- `who`: company, service branch, testers.
- `what`: tested system and result.
- `when`: test date or announcement date.
- `why`: qualification, deployment, capability validation.
- `how`: test profile, scenarios, evaluation process.

## MS05 Construction Deadline

Trigger:

- Phrases meaning complete by a deadline, build, construct, deploy at a site, plan.

Action:

- Center event type: `construction`.
- Predicate: `build` or `complete`.
- `who`: responsible country, ministry, service, or company.
- `what`: facility, radar, base, system.
- `when`: deadline or plan horizon.
- `where`: deployment or construction site.
- `why`: warning, defense, coverage, modernization.
- `how`: construction plan or system type if explicit.

## MS06 Casualty Report

Trigger:

- Phrases meaning death, died from, complications, reported cases, announced death.

Action:

- Center event type: `casualty`.
- Predicate: `die` or `report_death`.
- `who`: victim and reporting institution if relevant.
- `what`: death or casualty event.
- `when`: death date and hospitalization sequence if central.
- `where`: ship, base, hospital, region.
- `why`: disease, attack, accident, stated cause.
- `how`: mechanism of death only if explicit.

## MS07 First Deployment

Trigger:

- Phrases meaning first deployment, first time deployed, arrived, carried by a platform.

Action:

- Center event type: `deployment`.
- Predicate: `deploy`.
- `who`: deploying force or platform.
- `what`: deployed system.
- `when`: deployment date if explicit.
- `where`: theater, sea area, base, region.
- `why`: crisis, deterrence, mission need if explicit.
- `how`: carrier ship, aircraft, unit, route.

## MS08 Project Briefing

Trigger:

- Phrases meaning brief industry, introduce a program, describe vision and mission, budget, solicitation, operation and support.

Action:

- Center event type: `briefing`.
- Predicate: `brief`.
- `who`: program office, center, experts.
- `what`: project or program.
- `when`: briefing date.
- `where`: briefing venue.
- `why`: industry engagement, procurement, development.
- `how`: closed briefing, information-sharing, solicitation process.

## MS09 Capability Advantage

Trigger:

- Phrases meaning main advantage, can, able to, this means, high accuracy, improved range, improved capability.

Action:

- Do not create a new event unless capability is the paragraph focus.
- Attach capability to `what`.
- Attach operational value to `why`.
- Attach mechanism, platform, or subsystem to `how`.

## MS10 Reported Claim

Trigger:

- Phrases meaning said, stated, announced, according to reports, the report says.

Action:

- Determine whether the reporting act or the reported event is central.
- If the reporting act is central, source is `who/source`.
- If the reported event is central, source goes to evidence or `who/source`, and the event actor remains primary.
