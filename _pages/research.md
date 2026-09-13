---
layout: page
title: Research & Projects
permalink: /research/
description: Research and selected projects in collaborative XR, HCI, security, privacy, team cognition, and applied computing.
nav: true
nav_order: 1
---

My research asks how people build awareness, coordinate with others, and make security- and privacy-relevant decisions in immersive collaborative systems. I approach these questions through mixed-methods HCI research, controlled studies, interactive system design, and qualitative and quantitative analysis.

## Current research

### Collective situational awareness in asymmetric MR

**How does communication modality shape what collaborators notice, understand, and anticipate together?**

I led an end-to-end investigation of collective situational awareness in asymmetric mixed reality, designing and implementing a networked HoloLens 2 experiment and refining the protocol through a 12-participant pilot before conducting an IRB-approved, counterbalanced study with **48 participants across 24 dyads**.

The work extends SAGAT-based collective situation-awareness assessment with team-level measures of **information coverage** and **accurate alignment**, alongside correctness and response-alignment measures. I also built multimodal analysis pipelines integrating gaze, speech, SAGAT, workload, and performance data. The study found that **Gaze+Voice improved task performance and shared awareness**, while **Gaze-only produced the strongest spatial gaze convergence**, suggesting that performance, co-attention, and collective awareness capture distinct aspects of collaboration. The manuscript is under review at **IEEE VR 2027**.

### Security attacks in remote collaborative MR

**How do collaborators recognize and respond to attacks in shared immersive environments?**

I designed and executed a mixed-methods security study on remote collaborative MR, iteratively refining the task and attack conditions across two pilot studies before conducting an IRB-approved main study with **20 participants across 10 dyads**. I engineered four real-time attacks in a networked Unity/HoloLens 2 platform, including a novel click-redirection mechanism and MR-specific occlusion attacks.

By triangulating first-person recordings, behavioral observations, questionnaires, and interviews, the study uncovered gaps between users' perceived and actual security behavior. The resulting design recommendations focus on immersive security indicators, interaction transparency, and user training. This work resulted in my **first-author IEEE VR 2025 paper** and was featured in *Computerworld*.

### Privacy indicators for XR bystanders

**How should XR systems communicate privacy-relevant information when visual cues alone are insufficient?**

I collaborated on an iterative mixed-methods study of privacy indicators for situationally impaired XR bystanders. Four focus groups with 8 participants informed five visual and multimodal concepts, followed by a 7-participant evaluation of usability and contextual usefulness. The results showed limitations of visual-only cues under situational impairment and stronger preferences for multimodal indicators in privacy-sensitive scenarios. This work was published at **IEEE ISMAR Adjunct 2025**.

## Selected earlier projects

Before my PhD work, I built research and software systems spanning computer vision, remote sensing, GIS, healthcare, and full-stack development. A few selected projects are highlighted below.

<div class="projects">
{% assign sorted_projects = site.projects | sort: "importance" %}
<div class="row row-cols-1 row-cols-md-2">
{% for project in sorted_projects %}
  {% include projects.liquid %}
{% endfor %}
</div>
</div>
