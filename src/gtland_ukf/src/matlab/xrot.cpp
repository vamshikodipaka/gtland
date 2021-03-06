//
// File: xrot.cpp
//
// MATLAB Coder version            : 3.1
// C/C++ source code generated on  : 18-Oct-2017 21:20:19
//

// Include Files
#include "rt_nonfinite.h"
#include "UKF_main_c.h"
#include "xrot.h"

// Function Definitions

//
// Arguments    : int n
//                double x[36]
//                int ix0
//                int iy0
//                double c
//                double s
// Return Type  : void
//
void xrot(int n, double x[36], int ix0, int iy0, double c, double s)
{
  int ix;
  int iy;
  int k;
  double temp;
  if (n < 1) {
  } else {
    ix = ix0 - 1;
    iy = iy0 - 1;
    for (k = 1; k <= n; k++) {
      temp = c * x[ix] + s * x[iy];
      x[iy] = c * x[iy] - s * x[ix];
      x[ix] = temp;
      iy += 6;
      ix += 6;
    }
  }
}

//
// File trailer for xrot.cpp
//
// [EOF]
//
