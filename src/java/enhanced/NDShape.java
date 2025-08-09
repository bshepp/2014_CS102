import java.util.Arrays;
import java.math.BigDecimal;
import java.math.MathContext;

/**
 * Abstract base class for n-dimensional geometric shapes
 * Provides core functionality for shapes in arbitrary dimensions
 */
public abstract class NDShape {
    protected final int dimensions;
    protected final double[] parameters;
    
    protected NDShape(int dimensions, double... parameters) {
        if (dimensions < 1) {
            throw new IllegalArgumentException("Dimensions must be positive");
        }
        this.dimensions = dimensions;
        this.parameters = Arrays.copyOf(parameters, parameters.length);
        validateParameters();
    }
    
    /**
     * Validate shape-specific parameters
     */
    protected abstract void validateParameters();
    
    /**
     * Calculate the n-dimensional volume (hypervolume)
     */
    public abstract double getVolume();
    
    /**
     * Calculate the (n-1)-dimensional surface area
     */
    public abstract double getSurfaceArea();
    
    /**
     * Get the number of dimensions
     */
    public int getDimensions() {
        return dimensions;
    }
    
    /**
     * Get shape parameters
     */
    public double[] getParameters() {
        return Arrays.copyOf(parameters, parameters.length);
    }
    
    /**
     * Calculate gamma function for non-integer values
     * Used in n-dimensional volume calculations
     */
    protected static double gamma(double x) {
        if (x == 0.5) {
            return Math.sqrt(Math.PI);
        }
        if (x == 1.0) {
            return 1.0;
        }
        if (x > 1.0) {
            return (x - 1) * gamma(x - 1);
        }
        
        // Stirling's approximation for large values
        if (x > 10) {
            return Math.sqrt(2 * Math.PI / x) * Math.pow(x / Math.E, x);
        }
        
        // Use reflection formula for x < 1
        return Math.PI / (Math.sin(Math.PI * x) * gamma(1 - x));
    }
    
    /**
     * Calculate n-dimensional unit sphere volume coefficient
     */
    protected static double unitSphereVolume(int n) {
        if (n % 2 == 0) {
            // Even dimensions: V_n = π^(n/2) / (n/2)!
            double result = Math.pow(Math.PI, n / 2.0);
            for (int i = 1; i <= n / 2; i++) {
                result /= i;
            }
            return result;
        } else {
            // Odd dimensions: V_n = 2^((n+1)/2) * π^((n-1)/2) / (n!!)
            double result = Math.pow(2, (n + 1) / 2.0) * Math.pow(Math.PI, (n - 1) / 2.0);
            for (int i = n; i >= 1; i -= 2) {
                result /= i;
            }
            return result;
        }
    }
    
    /**
     * Get shape type name
     */
    public abstract String getShapeType();
    
    /**
     * Get mathematical formula for volume
     */
    public abstract String getVolumeFormula();
    
    /**
     * Get mathematical formula for surface area
     */
    public abstract String getSurfaceAreaFormula();
    
    @Override
    public String toString() {
        return String.format("%s (dim=%d): Volume=%.6f, Surface Area=%.6f", 
                            getShapeType(), dimensions, getVolume(), getSurfaceArea());
    }
}