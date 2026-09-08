(() => {
  'use strict';

  const menu = document.querySelector('.menu-toggle');
  const nav = document.getElementById('primary-nav');
  const mobile = window.matchMedia('(max-width: 900px)');

  if (menu && nav) {
    menu.hidden = false;
    document.body.classList.add('nav-enhanced');
    const closeMenu = () => {
      menu.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    });
    nav.addEventListener('click', event => {
      const link = event.target.closest('a');
      if (!link) return;
      closeMenu();
      if (mobile.matches) {
        // Move keyboard focus out of the now-collapsed navigation.
        const target = document.querySelector(link.getAttribute('href'));
        if (target) {
          target.setAttribute('tabindex', '-1');
          target.focus({ preventScroll: true });
        }
      }
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
        closeMenu();
        menu.focus();
      }
    });
    document.addEventListener('click', event => {
      if (!event.target.closest('.topbar')) closeMenu();
    });
    mobile.addEventListener('change', closeMenu);
  }

  // Authored fictional examples, not a live inference service.
  const examples = {
  "pt": {
    "title": "Physical therapy · routine visit",
    "transcript": "PT f/u. Pt reports easier chair transfers, still unsteady with turns. Gait w RW, CGA; better foot clearance after cues. Practiced sit-to-stand, less UE push-off. Continue skilled gait/balance work per POC.",
    "note": "The patient reports improved ease with chair transfers but continues to feel unsteady when turning. Skilled physical therapy focused on gait and transfer training. During ambulation with a rolling walker, the patient required contact guard assistance and demonstrated improved foot clearance following cueing. Sit-to-stand practice was completed with reduced reliance on upper-extremity push-off. Ongoing difficulty with turning and the need for cueing and guarding support continued skilled intervention for safe mobility. Gait and balance training will continue in accordance with the established plan of care.",
    "kind": "Illustrative draft"
  },
  "ot": {
    "title": "Occupational therapy · self-care visit",
    "transcript": "OT f/u. LB dressing w reacher, min A. Sequencing better after demo. Standing self-care limited by fatigue; pacing/rest cues helped. Needs reinforcement for independent carryover. Cont per POC.",
    "note": "Skilled occupational therapy addressed lower-body dressing and activity tolerance during self-care. The patient used a reacher for dressing and required minimal assistance. Task sequencing improved following demonstration, with reinforcement still needed for independent carryover. Fatigue limited standing self-care activities; cues for pacing and rest breaks helped the patient manage activity demands. Continued skilled intervention will focus on reinforcing dressing techniques and pacing strategies to support greater independence with daily routines. Treatment will continue according to the established plan of care.",
    "kind": "Illustrative draft"
  },
  "slp": {
    "title": "Speech therapy · communication visit",
    "transcript": "ST f/u. Pt loses train of thought on phone. Practiced brief call script w written keywords; more complete messages after rehearsal. Spouse used extra wait time. Needs skilled strategy training for carryover. Cont POC.",
    "note": "The patient reports losing their train of thought during telephone conversations. Skilled speech therapy focused on organizing and communicating messages using a brief call script and written keywords. Following rehearsal, the patient conveyed more complete messages. The spouse used additional wait time to support the patient during communication practice. Continued skilled strategy training is needed to promote carryover of these supports into telephone conversations. Treatment will continue under the established plan of care, with emphasis on functional communication and use of the practiced strategies.",
    "kind": "Illustrative draft"
  },
  "sn": {
    "title": "Skilled nursing · medication teaching",
    "transcript": "SN f/u. Med list reviewed; pt unsure of timing. Used written schedule and teach-back. Pt explained AM meds correctly, needed prompts for evening schedule. Reinforcement needed for safe med management. Cont teaching per POC.",
    "note": "Skilled nursing reviewed the medication list and addressed the patient’s uncertainty about medication timing. A written schedule was used to guide teaching, followed by teach-back to assess understanding. The patient correctly explained the morning medication schedule but required prompting for the evening schedule. Teaching remains incomplete, with further reinforcement needed to support safe medication management. Skilled nursing will continue medication education according to the established plan of care, with attention to the evening schedule and the patient’s ability to explain it independently.",
    "kind": "Illustrative draft"
  }
};

  const buttons = document.querySelectorAll('[data-example]');
  const transcript = document.getElementById('demo-transcript');
  const note = document.getElementById('demo-note');
  const noteTitle = document.getElementById('demo-note-title');
  const exampleKind = document.getElementById('demo-kind');
  if (buttons.length && transcript && note && noteTitle && exampleKind) {
    document.body.classList.add('demo-enhanced');
    buttons.forEach(button => {
      button.addEventListener('click', () => {
        const example = examples[button.dataset.example];
        if (!example) return;
        buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        transcript.textContent = '“' + example.transcript + '”';
        noteTitle.textContent = example.title;
        note.textContent = example.note;
        exampleKind.textContent = example.kind;
      });
    });
  }

  const year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());
})();
