// Placeholder report template for a Polar Bear calorimetry run.
//
// functions/compile_report.py copies this file, the summary JSON and the work-curve PNG
// side by side into the run's own folder, and the repo's assets/ folder once into the
// results root above it, which is the Typst root. A bare path below is therefore relative
// to the run's folder, and a path starting "/" is relative to the results root - which is
// where anything this template loads from disk must live, under /assets/. Edit THIS file,
// not the per-run copy.
//
// Fields available on `run`:
//   run.samples       int    samples recorded
//   run.duration_min  float  minutes from the first sample to the last
//   run.baseline_w    float  mean Q_abs over the selected baseline zone; past +/-10 W the
//                            cooling curve wants recalibrating
//   run.peak_w        float  largest excursion of Q_relative, sign preserved
//   run.energy_j      float  total energy change - the headline figure
//   run.direction      str   "added to" or "removed from"
//   run.plot           str   filename of the work-curve PNG
//   run.finished       str   ISO timestamp the report was generated
//
// The operator picks both zones by hand once the run ends. Each is described by a
// dictionary, run.baseline and run.experiment, with the same fields:
//   .start_min .end_min .duration_min   float  extent of the zone
//   .samples                            int    readings inside it
//   .mean .sd .spread                   float  of Q_abs in the baseline zone,
//                                              of Q_relative in the experiment zone
// A wide baseline .sd or .spread means the zone missed whole cycles of the 90-120 s
// power swing, so run.baseline_w (which is run.baseline.mean) is off-centre.

#let run = json(sys.inputs.data)

#set page(
  paper: "a4", 
  margin: 2cm,
  background: align(top, align(right, (box(image("/assets/CRD Logo.png", width: 2cm), inset: 2cm))))
  )
#set par(justify: false)
#set table(inset: (left: 0pt, rest: 5pt))

= Calorimetry report

Started at: #run.finished

Baseline zone parameters

#table(
  columns: (auto, auto),
  stroke: none,
  [Samples], [#run.baseline.samples],
  [Duration], [#run.baseline.duration_min min],
  [Start], [#run.baseline.start_min min],
  [σ], [#run.baseline.sd W]
)

Experiment parameters

#table(
  columns: (auto, auto),
  stroke: none,
  [Samples], [#run.experiment.samples],
  [Duration], [#run.experiment.duration_min min],
  [Baseline $Q_"abs"$], [#run.baseline_w W],
  [Peak $Q_"relative"$], [#run.peak_w W],
)

#text(size: 14pt)[
  *#run.energy_j J* (#calc.round(calc.abs(run.energy_j / 1000), digits: 3) kJ #run.direction the plate)
]

// The steady-state curve only holds at equilibrium, so the energy integral above is
// the robust number; the trace below shows how far each instant strayed.
#image(run.plot, width: 100%)
#pagebreak()

= Note

Sign convention:

Exothermic: +ve — heat transferred from reaction to plate

Endothermic: −ve — heat transferred from plate to reaction

The reported data from the Polar Bear Calorimeter is Energy transferred to/from the Polar Bear rather than ΔH of a reaction.

#image("/assets/sign-convention-diagram.png", width: 100%)