/**
 * N-dimensional hypercube implementation
 * Generalizes the concept of a cube to arbitrary dimensions
 */
public class HyperCube extends NDShape {
    private final double sideLength;
    
    public HyperCube(int dimensions, double sideLength) {
        super(dimensions, sideLength);
        this.sideLength = sideLength;
    }
    
    @Override
    protected void validateParameters() {
        if (parameters.length != 1) {
            throw new IllegalArgumentException("HyperCube requires exactly one parameter (side length)");
        }
        if (parameters[0] < 0) {
            throw new IllegalArgumentException("Side length cannot be negative");
        }
    }
    
    @Override
    public double getVolume() {
        return Math.pow(sideLength, dimensions);
    }
    
    @Override
    public double getSurfaceArea() {
        if (dimensions == 0) return 0;
        if (dimensions == 1) return 2; // Two endpoints
        
        // Surface area = 2n × s^(n-1) where n is dimensions, s is side length
        return 2 * dimensions * Math.pow(sideLength, dimensions - 1);
    }
    
    public double getSideLength() {
        return sideLength;
    }
    
    /**
     * Get the number of vertices in the hypercube
     */
    public int getVertexCount() {
        return (int) Math.pow(2, dimensions);
    }
    
    /**
     * Get the number of edges in the hypercube
     */
    public int getEdgeCount() {
        return dimensions * (int) Math.pow(2, dimensions - 1);
    }
    
    /**
     * Get the number of k-dimensional faces
     */
    public int getFaceCount(int k) {
        if (k < 0 || k > dimensions) return 0;
        
        // Number of k-faces = C(n,k) * 2^(n-k)
        return binomial(dimensions, k) * (int) Math.pow(2, dimensions - k);
    }
    
    private int binomial(int n, int k) {
        if (k > n || k < 0) return 0;
        if (k == 0 || k == n) return 1;
        
        int result = 1;
        for (int i = 1; i <= k; i++) {
            result = result * (n - i + 1) / i;
        }
        return result;
    }
    
    @Override
    public String getShapeType() {
        return "HyperCube";
    }
    
    @Override
    public String getVolumeFormula() {
        return String.format("V_%d = s^%d", dimensions, dimensions);
    }
    
    @Override
    public String getSurfaceAreaFormula() {
        if (dimensions == 1) return "S₁ = 2";
        return String.format("S_%d = 2 × %d × s^%d", dimensions, dimensions, dimensions - 1);
    }
    
    /**
     * Calculate diagonal length through the hypercube
     */
    public double getDiagonal() {
        return sideLength * Math.sqrt(dimensions);
    }
    
    /**
     * Check if a point is inside the hypercube
     */
    public boolean contains(double[] point) {
        if (point.length != dimensions) {
            throw new IllegalArgumentException("Point dimension mismatch");
        }
        
        for (double coord : point) {
            if (coord < 0 || coord > sideLength) {
                return false;
            }
        }
        return true;
    }
    
    @Override
    public String toString() {
        return String.format("%s (dim=%d, side=%.3f): Volume=%.6f, Surface Area=%.6f, Vertices=%d", 
                            getShapeType(), dimensions, sideLength, getVolume(), getSurfaceArea(), getVertexCount());
    }
}