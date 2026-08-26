// Placeholder report template for a Polar Bear calorimetry run.
//
// functions/compile_report.py copies this file, the summary JSON, the work-curve PNG
// and the repo's assets/ folder side by side into the run's results folder, and compiles
// them there. Every path below is therefore relative to that folder, and anything this
// template loads from disk must live in assets/. Edit THIS file, not the per-run copy.
//
// Fields available on `run`:
//   run.samples       int    samples recorded
//   run.duration_min  float  minutes from the first sample to the last
//   run.baseline_w    float  Q_abs at t=0; past +/-10 W the cooling curve wants recalibrating
//   run.peak_w        float  largest excursion of Q_relative, sign preserved
//   run.energy_j      float  total energy change - the headline figure
//   run.direction      str   "added to" or "removed from"
//   run.plot           str   filename of the work-curve PNG
//   run.finished       str   ISO timestamp the report was generated

#let run = json(sys.inputs.data)

#set page(
  paper: "a4", 
  margin: 2cm,
  background: align(top, align(right, (box(image("assets/CRD Logo.png", width: 2cm), inset: 2cm))))
  )
#set par(justify: true)

= Calorimetry report

Started at: #run.finished

// PLACEHOLDER LAYOUT - replace everything below with your own.

#table(
  columns: (auto, auto),
  stroke: none,
  [Samples], [#run.samples],
  [Duration], [#run.duration_min min],
  [Baseline $Q_"abs"$], [#run.baseline_w W],
  [Peak $Q_"relative"$], [#run.peak_w W],
)

#text(size: 14pt)[
  *#run.energy_j J* (#calc.round(calc.abs(run.energy_j / 1000), digits: 3) kJ #run.direction the plate)
]

// The steady-state curve only holds at equilibrium, so the energy integral above is
// the robust number; the trace below shows how far each instant strayed.
#image(run.plot, width: 100%)
