//Brian Sheppard
//10/02/2014
//Project 4. PP 4.1a
//Released under the MIT License; see LICENSE for details.
import java.text.DecimalFormat;


/**
 * Represents a sphere and provides methods for working with
 * its diameter, surface area and volume.
 */
public class Sphere
{
   /** Current diameter of the sphere */
   private double diameter;

   /**
    * Creates a Sphere using the provided initial diameter.
    * The constructor also precomputes the volume and area
    * from this starting diameter.
    *
    * @param initial starting diameter value
    */
   public Sphere (double initial)
   {
      setDiameter(initial);
   }

   /**
    * Updates the sphere's diameter.
    *
    * @param newdiameter the new diameter value
    */
   public void setDiameter (double newdiameter)
   {
      if (newdiameter < 0) {
         throw new IllegalArgumentException("Diameter cannot be negative");
      }
      diameter = newdiameter;
   }

   /**
    * Retrieves the current diameter of the sphere.
    *
    * @return diameter value
    */
   public double getDiameter ()
   {
      return diameter;
   }

   /**
    * Calculates the volume using the current diameter.
    *
    * @return sphere volume
    */
   public double getVolume ()
   {
      double volume = (4.0/3.0) * Math.PI * Math.pow((0.5 * diameter), 3);
      return volume;
   }

   /**
    * Calculates the surface area using the current diameter.
    *
    * @return sphere surface area
    */
   public double getArea ()
   {
      double area = 4.0 * Math.PI * Math.pow((0.5 * diameter), 2);
      return area;
   }

   /**
    * Returns a string describing the initially computed
    * volume and surface area.
    */
   public String toString ()
   {
      DecimalFormat fmt = new DecimalFormat ("0.###");
   
      return "a volume of " + fmt.format(getVolume()) + ", and an area of " + fmt.format(getArea()) + ".";
   }
}
