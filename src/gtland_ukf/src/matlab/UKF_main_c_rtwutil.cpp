//
// File: UKF_main_c_rtwutil.cpp
//
// MATLAB Coder version            : 3.1
// C/C++ source code generated on  : 18-Oct-2017 21:20:19
//

// Include Files
#include "rt_nonfinite.h"
#include "UKF_main_c.h"
#include "UKF_main_c_rtwutil.h"

// Function Definitions

//
// Arguments    : double u0
//                double u1
// Return Type  : double
//
double rt_hypotd_snf(double u0, double u1)
{
  double y;
  double a;
  double b;
  a = fabs(u0);
  b = fabs(u1);
  if (a < b) {
    a /= b;
    y = b * sqrt(a * a + 1.0);
  } else if (a > b) {
    b /= a;
    y = a * sqrt(b * b + 1.0);
  } else if (rtIsNaN(b)) {
    y = b;
  } else {
    y = a * 1.4142135623730951;
  }

  return y;
}

//
// File trailer for UKF_main_c_rtwutil.cpp
//
// [EOF]
//
