//Brian Sheppard
//10/04/2014
//Project 4. PP 4.1b

import java.util.Scanner;
import java.text.DecimalFormat;

/**
 * Driver program that interacts with the user and displays
 * the calculated surface area and volume of a sphere.
 */
public class MultiSphere
{
   /**
    * Application entry point.
    *
    * @param args command line arguments (not used)
    */
   public static void main (String[] args)
   {
      // Variables used to store calculated values
      double spherev, spherea, spherediameter, diameterinput;

      // Read user input from the console
      Scanner scan = new Scanner (System.in);

      // Sphere instance starting with a default diameter of 1
      Sphere usersphere = new Sphere(1);

      // Formatter to limit decimals in the output
      DecimalFormat fmt = new DecimalFormat ("0.###");

      // Demonstrate the results for a sphere with a diameter of 1
      usersphere.setDiameter(1);
      System.out.println("A sphere with a diameter of 1 has " + usersphere + "");
      System.out.println();

      // Prompt for a custom diameter
      System.out.println("Please enter the diameter of your sphere.");
      diameterinput = scan.nextDouble();
      usersphere.setDiameter(diameterinput);

      // Calculate surface area using the user's diameter
      spherea = usersphere.getArea();

      // Store the diameter for formatted output
      spherediameter = usersphere.getDiameter();

      // Display the surface area
      System.out.println("The surface area of a sphere with diameter of " +
                         fmt.format(spherediameter) + " is " +
                         fmt.format(spherea) + ".");
      System.out.println();

      // Calculate and display the volume
      spherev = usersphere.getVolume();
      System.out.println("The volume of a sphere with diameter of " +
                         fmt.format(spherediameter) + " is " +
                         fmt.format(spherev) + ".");

   }
}

