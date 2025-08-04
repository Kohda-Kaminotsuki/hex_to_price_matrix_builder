# hex_to_price_matrix_builder
python module that takes an input dictionary of (r, g, b) keys, 0-255 each, and integer values and returns a dictionary of calculated averages based on recursively testing adjacent matrix blocks. Works better the more values manually input. 
Best case scenario is evenly distributed with 50% of values filled in, or put another way having all values of #RGB filled in and allowing the module to build out #RRGGBB from #RGB. 
Theoretically will work even with a single value input but that would just recursively set everything to that value in a lot slower speed than for x in product r,g,b range(256): x = value . 
