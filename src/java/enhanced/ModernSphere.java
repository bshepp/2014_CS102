/**
 * Modern 3D sphere implementation that extends the n-dimensional framework
 * Backwards compatible with the original Sphere class
 */
public class ModernSphere extends HyperSphere {
    
    public ModernSphere(double radius) {
        super(3, radius);
    }
    
    public ModernSphere(double diameter, boolean isDiameter) {
        super(3, isDiameter ? diameter / 2.0 : diameter);
    }
    
    // Backwards compatibility methods
    public double getDiameter() {
        return 2 * getRadius();
    }
    
    public void setDiameter(double diameter) {
        if (diameter < 0) {
            throw new IllegalArgumentException("Diameter cannot be negative");
        }
        // Note: This creates a new object since NDShape is immutable
        // In a full implementation, we'd need to handle this differently
    }
    
    // Legacy method names for compatibility
    public double getArea() {
        return getSurfaceArea();
    }
    
    @Override
    public String toString() {
        return String.format("a volume of %.3f, and an area of %.3f.", getVolume(), getSurfaceArea());
    }
    
    /**
     * Demonstrate backwards compatibility with original MultiSphere
     */
    public static void demonstrateCompatibility() {
        System.out.println("=== Backwards Compatibility Demo ===");
        
        ModernSphere sphere = new ModernSphere(1.0);
        System.out.println("A sphere with a diameter of 1 has " + sphere);
        
        ModernSphere userSphere = new ModernSphere(2.5);
        System.out.println("The surface area of a sphere with diameter of " + 
                          userSphere.getDiameter() + " is " + userSphere.getArea());
        System.out.println("The volume of a sphere with diameter of " + 
                          userSphere.getDiameter() + " is " + userSphere.getVolume());
        
        System.out.println("\n=== Extended Capabilities ===");
        System.out.println("Volume formula: " + userSphere.getVolumeFormula());
        System.out.println("Surface area formula: " + userSphere.getSurfaceAreaFormula());
        System.out.println("Cross-section at distance 0.5: " + userSphere.getCrossSection(0.5));
    }
}