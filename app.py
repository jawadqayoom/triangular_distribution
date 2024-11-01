from flask import Flask, request, render_template
import numpy as np
import matplotlib.pyplot as plt
import io
import base64  

app = Flask(__name__)

# Function to calculate probability using the area of a triangle method
def triangular_area_probability(a, b, c, threshold):
    # If the threshold is outside the range [a, b], handle those cases directly
    if threshold <= a:
        return 0.0
    elif threshold >= b:
        return 1.0
    
    # Check if the threshold lies in the left or right segment
    if threshold <= c:
        # Left triangle area from a to threshold
        base_left = threshold - a
        height_left = (2 / (b - a) ) * ( (threshold - a) / (c - a) )
        area_left = 0.5 * base_left * height_left
        return area_left
    else:
        # Right triangle area from threshold to b
        base_right = b - threshold
        height_right = (2 / (b - c) ) * ( (b - threshold) / (b - a) )
        area_right = 0.5 * base_right * height_right
        return area_right
        
        

    

# Function to simulate samples and calculate probability using the triangle area method
def triangular_simulation(a, b, c, threshold, num_samples=2000):
    # Calculate the probability of weekly sales below the threshold using the area method
    prob = triangular_area_probability(a, b, c, threshold)
    
    # Simulate the triangular distribution using numpy for the histogram
    sales_samples = np.random.triangular(a, c, b, num_samples)
    
    return sales_samples, prob

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        a = int(request.form['a'])
        b = int(request.form['b'])
        c = int(request.form['c'])
        threshold = int(request.form.get('threshold', 2000))

        sales_samples, prob_under_threshold = triangular_simulation(a, b, c, threshold)

        if threshold < c:
            message = f"Probability of weekly sales under ${threshold}:"
        else:
            message = f"Probability of weekly sales above ${threshold}:"

        plt.figure()
        plt.hist(sales_samples, bins=30, color="lightblue", edgecolor="black")
        plt.axvline(threshold, color='red', linestyle='dashed', linewidth=2, label=f'Sales < {threshold}')
        plt.title("Distribution of Simulated Weekly Sales")
        plt.xlabel("Weekly Sales ($)")
        plt.ylabel("Frequency")
        plt.legend()
        
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        return render_template('result.html', prob=prob_under_threshold, graph_url=graph_url, message=message)
    
    except KeyError as e:
        return f"Missing form field: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)
