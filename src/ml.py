import numpy as np

class MLModelEquations:
    def __init__(self, degree=2):
        self.degree = degree

    def fit_equations(self, history):
        if len(history) < self.degree + 1:
            return None, None 

        t = np.arange(len(history))
        x_data = np.array([p.x for p in history])
        y_data = np.array([p.y for p in history])

        coeffs_x = np.polyfit(t, x_data, self.degree)
        coeffs_y = np.polyfit(t, y_data, self.degree)

        poly_x = np.poly1d(coeffs_x)
        poly_y = np.poly1d(coeffs_y)

        return poly_x, poly_y

    def poly_to_string(self, poly):
        s = ""
        degree = poly.order
        for i, coeff in enumerate(poly.coeffs):
            exp = degree - i
            if abs(coeff) < 1e-100:
                continue
            sign = " + " if coeff > 0 else " - "
            coeff_str = f"{abs(coeff):.3f}"
            if exp == 0:
                term = coeff_str
            elif exp == 1:
                term = coeff_str + "t"
            else:
                term = coeff_str + f"t^{exp}"
            s += sign + term
        if s.startswith(" + "):
            s = s[3:]
        return s

