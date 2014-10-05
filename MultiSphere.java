//Brian Sheppard
//10/04/2014
//Project 4. PP 4.1b

import java.util.Scanner;
import java.text.DecimalFormat;

public class MultiSphere
{
   public static void main (String[] args)
   {     
      double spherev, spherea, spherediameter, diameterinput;
      
      Scanner scan = new Scanner (System.in);
      Sphere usersphere = new Sphere(1);
      DecimalFormat fmt = new DecimalFormat ("0.###");
      
      usersphere.setDiameter(1);
      System.out.println("A sphere with a diameter of 1 has " + usersphere + "");
      System.out.println();
     
      System.out.println("Please enter the diameter of your sphere.");
      diameterinput = scan.nextDouble();
      usersphere.setDiameter(diameterinput);
      
      spherea = usersphere.getArea();
      spherediameter = usersphere.getDiameter();
      System.out.println("The surface area of a sphere with diameter of " + fmt.format(spherediameter) + " is " + fmt.format(spherea) + ".");
      System.out.println();
      spherev = usersphere.getVolume();
      System.out.println("The volume of a sphere with diameter of " + fmt.format(spherediameter) + " is " + fmt.format(spherev) + ".");
      
   }
}

