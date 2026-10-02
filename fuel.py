from scipy.interpolate import interp1d

fuel_values = [
500,1000,1500,2000,2500,3000,3500,4000,
4500,5000,5500,6000,6500,7000,7500,8000,
8500,8700,9000,9500,10000,10500,11000,
11500,12000,12500,13000,13500,14000,
14500,15000,15500,15700
]

fuel_index = [
-0.7,-1.3,-1.9,-2.3,-2.7,-3.1,-3.4,-3.7,
-4.1,-4.4,-4.6,-4.5,-4.0,-3.2,-1.9,0,
2.5,3.8,3.2,2.3,1.3,0.3,-0.7,-1.6,
-2.6,-3.6,-4.6,-5.5,-6.5,-7.5,-8.6,
-9.9,-10.5
]

interpolation = interp1d(
    fuel_values,
    fuel_index,
    fill_value="extrapolate"
)

def get_fuel_index(fuel):
    return float(interpolation(fuel))