import java.util.*;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.text.DecimalFormat;

/**
 * Agentic interface for natural language geometry queries
 * Parses user requests and performs geometric calculations
 */
public class GeometryAgent {
    private final DecimalFormat formatter = new DecimalFormat("#.######");
    private final Map<String, NDShape> savedShapes = new HashMap<>();
    private int shapeCounter = 1;
    
    /**
     * Process a natural language query about geometry
     */
    public String processQuery(String query) {
        query = query.toLowerCase().trim();
        
        try {
            // Create shape queries
            if (query.contains("create") || query.contains("make")) {
                return handleCreateQuery(query);
            }
            
            // Property queries
            if (query.contains("volume") || query.contains("area") || query.contains("surface")) {
                return handlePropertyQuery(query);
            }
            
            // Comparison queries
            if (query.contains("compare") || query.contains("vs") || query.contains("versus")) {
                return handleComparisonQuery(query);
            }
            
            // Dimensional analysis
            if (query.contains("dimension") || query.contains("how does") || query.contains("scale")) {
                return handleDimensionalAnalysis(query);
            }
            
            // Mathematical explanation
            if (query.contains("explain") || query.contains("formula") || query.contains("why")) {
                return handleExplanationQuery(query);
            }
            
            // List saved shapes
            if (query.contains("list") || query.contains("show")) {
                return listSavedShapes();
            }
            
            return "I can help you with:\n" +
                   "• Creating shapes: 'create a 4D sphere with radius 2'\n" +
                   "• Calculating properties: 'what's the volume of a 3D cube with side 5?'\n" +
                   "• Comparisons: 'compare sphere vs cube in 4 dimensions'\n" +
                   "• Dimensional analysis: 'how does volume scale with dimension?'\n" +
                   "• Explanations: 'explain the formula for 5D sphere volume'\n" +
                   "• Listing shapes: 'show all saved shapes'";
                   
        } catch (Exception e) {
            return "Sorry, I encountered an error: " + e.getMessage();
        }
    }
    
    private String handleCreateQuery(String query) {
        // Extract shape type
        String shapeType = "sphere";
        if (query.contains("cube") || query.contains("hypercube")) {
            shapeType = "cube";
        }
        
        // Extract dimensions
        int dimensions = extractDimensions(query);
        if (dimensions == -1) {
            return "Please specify the number of dimensions (e.g., '3D', '4-dimensional')";
        }
        
        // Extract parameter
        double parameter = extractParameter(query);
        if (parameter == -1) {
            return "Please specify the " + (shapeType.equals("sphere") ? "radius" : "side length");
        }
        
        NDShape shape;
        String paramName;
        
        if (shapeType.equals("sphere")) {
            shape = new HyperSphere(dimensions, parameter);
            paramName = "radius";
        } else {
            shape = new HyperCube(dimensions, parameter);
            paramName = "side length";
        }
        
        String shapeName = "shape" + shapeCounter++;
        savedShapes.put(shapeName, shape);
        
        return String.format("Created %s '%s':\n%s\n%s = %s\nFormulas:\n• %s\n• %s",
                           shape.getShapeType(), shapeName, shape.toString(), 
                           paramName, formatter.format(parameter),
                           shape.getVolumeFormula(), shape.getSurfaceAreaFormula());
    }
    
    private String handlePropertyQuery(String query) {
        String shapeType = "sphere";
        if (query.contains("cube") || query.contains("hypercube")) {
            shapeType = "cube";
        }
        
        int dimensions = extractDimensions(query);
        double parameter = extractParameter(query);
        
        if (dimensions == -1 || parameter == -1) {
            return "Please specify both dimensions and parameter (radius or side length)";
        }
        
        NDShape shape = shapeType.equals("sphere") 
            ? new HyperSphere(dimensions, parameter)
            : new HyperCube(dimensions, parameter);
        
        StringBuilder response = new StringBuilder();
        
        if (query.contains("volume")) {
            response.append(String.format("Volume of %dD %s: %s\n", 
                          dimensions, shapeType, formatter.format(shape.getVolume())));
            response.append("Formula: ").append(shape.getVolumeFormula());
        }
        
        if (query.contains("area") || query.contains("surface")) {
            if (response.length() > 0) response.append("\n");
            response.append(String.format("Surface area of %dD %s: %s\n", 
                          dimensions, shapeType, formatter.format(shape.getSurfaceArea())));
            response.append("Formula: ").append(shape.getSurfaceAreaFormula());
        }
        
        if (response.length() == 0) {
            response.append(shape.toString());
        }
        
        return response.toString();
    }
    
    private String handleComparisonQuery(String query) {
        int dimensions = extractDimensions(query);
        double parameter = extractParameter(query);
        
        if (dimensions == -1 || parameter == -1) {
            dimensions = 3;
            parameter = 1.0;
        }
        
        HyperSphere sphere = new HyperSphere(dimensions, parameter);
        HyperCube cube = new HyperCube(dimensions, parameter);
        
        double sphereVolume = sphere.getVolume();
        double cubeVolume = cube.getVolume();
        double sphereArea = sphere.getSurfaceArea();
        double cubeArea = cube.getSurfaceArea();
        
        return String.format("Comparison in %dD (parameter = %s):\n\n" +
                           "SPHERE:\n• Volume: %s\n• Surface Area: %s\n\n" +
                           "CUBE:\n• Volume: %s\n• Surface Area: %s\n\n" +
                           "RATIOS:\n• Volume ratio (sphere/cube): %s\n• Surface ratio (sphere/cube): %s",
                           dimensions, formatter.format(parameter),
                           formatter.format(sphereVolume), formatter.format(sphereArea),
                           formatter.format(cubeVolume), formatter.format(cubeArea),
                           formatter.format(sphereVolume / cubeVolume), 
                           formatter.format(sphereArea / cubeArea));
    }
    
    private String handleDimensionalAnalysis(String query) {
        if (query.contains("volume")) {
            return "Volume scaling with dimension:\n" +
                   "• For unit spheres: Volume peaks around 5-6 dimensions, then decreases\n" +
                   "• For unit cubes: Volume = 1 regardless of dimension\n" +
                   "• For fixed radius r: V_n ∝ r^n (grows exponentially with dimension)\n" +
                   "• Higher dimensions concentrate volume near the surface (curse of dimensionality)";
        }
        
        if (query.contains("surface") || query.contains("area")) {
            return "Surface area scaling with dimension:\n" +
                   "• For spheres: S_n = n × V_n / r (proportional to dimension)\n" +
                   "• For cubes: S_n = 2n × s^(n-1) (linear in dimension)\n" +
                   "• Surface-to-volume ratio increases with dimension";
        }
        
        return "Dimensional scaling insights:\n" +
               "• Most volume concentrates near the surface in high dimensions\n" +
               "• Distance between random points approaches constant value\n" +
               "• Optimization becomes harder (curse of dimensionality)\n" +
               "• Many geometric intuitions from 2D/3D break down";
    }
    
    private String handleExplanationQuery(String query) {
        int dimensions = extractDimensions(query);
        if (dimensions == -1) dimensions = 3;
        
        if (query.contains("sphere")) {
            return explainSphereFormula(dimensions);
        } else if (query.contains("cube")) {
            return explainCubeFormula(dimensions);
        }
        
        return "I can explain formulas for spheres and cubes in any dimension. " +
               "Try: 'explain 4D sphere formula' or 'explain cube volume formula'";
    }
    
    private String explainSphereFormula(int dimensions) {
        HyperSphere sphere = new HyperSphere(dimensions, 1.0);
        
        String explanation = String.format("N-dimensional sphere volume formula (n=%d):\n\n", dimensions);
        explanation += sphere.getVolumeFormula() + "\n\n";
        explanation += "Where:\n";
        explanation += "• The coefficient comes from integrating over the unit sphere\n";
        explanation += "• π^(n/2) appears from repeated integration in circular coordinates\n";
        explanation += "• Gamma function Γ(n/2+1) = (n/2)! for integer n/2\n";
        explanation += "• r^n shows volume scales as nth power of radius\n\n";
        
        if (dimensions <= 4) {
            explanation += "Special cases:\n";
            explanation += "• 1D: V₁ = 2r (line segment)\n";
            explanation += "• 2D: V₂ = πr² (circle)\n";
            explanation += "• 3D: V₃ = (4/3)πr³ (sphere)\n";
            explanation += "• 4D: V₄ = (π²/2)r⁴ (hypersphere)\n";
        }
        
        return explanation;
    }
    
    private String explainCubeFormula(int dimensions) {
        return String.format("N-dimensional cube volume formula (n=%d):\n\n" +
                           "V_n = s^n\n\n" +
                           "This is beautifully simple!\n" +
                           "• Each dimension contributes a factor of s\n" +
                           "• Volume is just side length raised to the nth power\n" +
                           "• Surface area: S_n = 2n × s^(n-1)\n" +
                           "• Number of vertices: 2^n\n" +
                           "• Number of edges: n × 2^(n-1)", dimensions);
    }
    
    private String listSavedShapes() {
        if (savedShapes.isEmpty()) {
            return "No shapes saved. Create some with 'create a 4D sphere with radius 2'";
        }
        
        StringBuilder list = new StringBuilder("Saved shapes:\n");
        for (Map.Entry<String, NDShape> entry : savedShapes.entrySet()) {
            list.append("• ").append(entry.getKey()).append(": ").append(entry.getValue()).append("\n");
        }
        return list.toString();
    }
    
    private int extractDimensions(String query) {
        Pattern pattern = Pattern.compile("(\\d+)\\s*d(?:imension)?|\\b(\\d+)\\s*dimensional");
        Matcher matcher = pattern.matcher(query);
        if (matcher.find()) {
            String dimStr = matcher.group(1) != null ? matcher.group(1) : matcher.group(2);
            return Integer.parseInt(dimStr);
        }
        return -1;
    }
    
    private double extractParameter(String query) {
        Pattern pattern = Pattern.compile("(?:radius|side|length)\\s*(?:of|=|is)?\\s*(\\d+(?:\\.\\d+)?)|\\b(\\d+(?:\\.\\d+)?)\\s*(?:radius|side|length)");
        Matcher matcher = pattern.matcher(query);
        if (matcher.find()) {
            String paramStr = matcher.group(1) != null ? matcher.group(1) : matcher.group(2);
            return Double.parseDouble(paramStr);
        }
        return -1;
    }
}