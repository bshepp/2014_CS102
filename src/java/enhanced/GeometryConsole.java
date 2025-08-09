import java.util.Scanner;

/**
 * Interactive console for the n-dimensional geometry engine
 * Demonstrates the agentic interface capabilities
 */
public class GeometryConsole {
    private static final GeometryAgent agent = new GeometryAgent();
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        printWelcome();
        
        while (true) {
            System.out.print("\n🌌 Geometry > ");
            String input = scanner.nextLine().trim();
            
            if (input.equalsIgnoreCase("quit") || input.equalsIgnoreCase("exit")) {
                System.out.println("Goodbye! Thanks for exploring n-dimensional geometry!");
                break;
            }
            
            if (input.equalsIgnoreCase("help")) {
                printHelp();
                continue;
            }
            
            if (input.equalsIgnoreCase("demo")) {
                runDemo();
                continue;
            }
            
            if (input.isEmpty()) {
                continue;
            }
            
            System.out.println("\n" + agent.processQuery(input));
        }
        
        scanner.close();
    }
    
    private static void printWelcome() {
        System.out.println("╔══════════════════════════════════════════════════════════════╗");
        System.out.println("║                N-DIMENSIONAL GEOMETRY ENGINE                 ║");
        System.out.println("║                    with Agentic Interface                   ║");
        System.out.println("╚══════════════════════════════════════════════════════════════╝");
        System.out.println();
        System.out.println("🚀 Welcome to the future of geometry! Ask me anything about");
        System.out.println("   shapes in any number of dimensions using natural language.");
        System.out.println();
        System.out.println("💡 Try: 'create a 5D sphere with radius 3'");
        System.out.println("   Or: 'compare sphere vs cube in 7 dimensions'");
        System.out.println("   Or: 'explain how volume scales with dimension'");
        System.out.println();
        System.out.println("Type 'help' for more examples, 'demo' for a showcase, or 'quit' to exit.");
    }
    
    private static void printHelp() {
        System.out.println("\n📚 HELP - Natural Language Commands");
        System.out.println("═══════════════════════════════════════");
        System.out.println();
        System.out.println("🏗️  CREATING SHAPES:");
        System.out.println("   • 'create a 4D sphere with radius 2'");
        System.out.println("   • 'make a 6-dimensional cube with side length 1.5'");
        System.out.println("   • 'create a 10D hypersphere radius 0.5'");
        System.out.println();
        System.out.println("📊 CALCULATING PROPERTIES:");
        System.out.println("   • 'what's the volume of a 3D sphere with radius 4?'");
        System.out.println("   • 'surface area of 5D cube side 2'");
        System.out.println("   • 'volume and area of 7-dimensional sphere radius 1'");
        System.out.println();
        System.out.println("⚖️  COMPARISONS:");
        System.out.println("   • 'compare sphere vs cube in 4 dimensions'");
        System.out.println("   • 'sphere versus cube 6D parameter 2'");
        System.out.println();
        System.out.println("🔍 DIMENSIONAL ANALYSIS:");
        System.out.println("   • 'how does volume scale with dimension?'");
        System.out.println("   • 'explain surface area scaling'");
        System.out.println("   • 'dimensional scaling insights'");
        System.out.println();
        System.out.println("🧠 EXPLANATIONS:");
        System.out.println("   • 'explain the formula for 5D sphere volume'");
        System.out.println("   • 'why does sphere volume peak at 5-6 dimensions?'");
        System.out.println("   • 'explain 4D cube formula'");
        System.out.println();
        System.out.println("📋 UTILITY:");
        System.out.println("   • 'list all saved shapes'");
        System.out.println("   • 'show saved shapes'");
    }
    
    private static void runDemo() {
        System.out.println("\n🎬 DEMO - Exploring Higher Dimensions");
        System.out.println("═══════════════════════════════════════════");
        
        String[] demoQueries = {
            "create a 3D sphere with radius 1",
            "create a 4D sphere with radius 1", 
            "create a 5D sphere with radius 1",
            "create a 10D sphere with radius 1",
            "compare sphere vs cube in 4 dimensions",
            "how does volume scale with dimension?",
            "explain the formula for 4D sphere volume"
        };
        
        for (String query : demoQueries) {
            System.out.println("\n🌌 Query: " + query);
            System.out.println("───────────────────────────────────");
            System.out.println(agent.processQuery(query));
            
            // Pause for readability
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("\n🎉 Demo complete! Try your own queries now.");
    }
}