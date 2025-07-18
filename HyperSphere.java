/**
 * N-dimensional hypersphere implementation
 * Generalizes the concept of a sphere to arbitrary dimensions
 */
public class HyperSphere extends NDShape {
    private final double radius;
    
    public HyperSphere(int dimensions, double radius) {
        super(dimensions, radius);
        this.radius = radius;
    }
    
    @Override
    protected void validateParameters() {
        if (parameters.length != 1) {
            throw new IllegalArgumentException("HyperSphere requires exactly one parameter (radius)");
        }
        if (parameters[0] < 0) {
            throw new IllegalArgumentException("Radius cannot be negative");
        }
    }
    
    @Override
    public double getVolume() {
        return unitSphereVolume(dimensions) * Math.pow(radius, dimensions);
    }
    
    @Override
    public double getSurfaceArea() {
        if (dimensions == 1) {
            return 2; // Two points
        }
        return dimensions * unitSphereVolume(dimensions) * Math.pow(radius, dimensions - 1);
    }
    
    public double getRadius() {
        return radius;
    }
    
    public double getDiameter() {
        return 2 * radius;
    }
    
    @Override
    public String getShapeType() {
        return "HyperSphere";
    }
    
    @Override
    public String getVolumeFormula() {
        if (dimensions == 1) return "V₁ = 2r";
        if (dimensions == 2) return "V₂ = πr²";
        if (dimensions == 3) return "V₃ = (4/3)πr³";
        if (dimensions == 4) return "V₄ = (π²/2)r⁴";
        
        if (dimensions % 2 == 0) {
            return String.format("V_%d = (π^%d/%d!) × r^%d", 
                               dimensions, dimensions/2, dimensions/2, dimensions);
        } else {
            return String.format("V_%d = (2^%d × π^%d)/(odd factors) × r^%d", 
                               dimensions, (dimensions+1)/2, (dimensions-1)/2, dimensions);
        }
    }
    
    @Override
    public String getSurfaceAreaFormula() {
        if (dimensions == 1) return "S₁ = 2";
        if (dimensions == 2) return "S₂ = 2πr";
        if (dimensions == 3) return "S₃ = 4πr²";
        if (dimensions == 4) return "S₄ = 2π²r³";
        
        return String.format("S_%d = %d × V_%d / r", dimensions, dimensions, dimensions);
    }
    
    /**
     * Calculate the volume of a cross-section at a given distance from center
     */
    public double getCrossSection(double distance) {
        if (Math.abs(distance) >= radius) {
            return 0;
        }
        
        double crossSectionRadius = Math.sqrt(radius * radius - distance * distance);
        if (dimensions == 1) {
            return 1; // Point
        }
        
        HyperSphere crossSection = new HyperSphere(dimensions - 1, crossSectionRadius);
        return crossSection.getVolume();
    }
    
    /**
     * Project to lower dimension (e.g., 4D sphere to 3D sphere)
     */
    public HyperSphere projectToLowerDimension() {
        if (dimensions <= 1) {
            throw new IllegalStateException("Cannot project 1D or lower");
        }
        return new HyperSphere(dimensions - 1, radius);
    }
}