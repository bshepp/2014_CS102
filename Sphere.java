//Brian Sheppard
//10/02/2014
//Project 4. PP 4.1a
import java.text.DecimalFormat;


public class Sphere
{
   private double diameter, spherev, spherea;   

   public Sphere (double initial)
   {
      diameter = initial;
      spherev = ((4.0/3.0) * Math.PI * Math.pow((0.5 * diameter), 3));
      spherea = (4.0 * Math.PI * Math.pow((0.5 * diameter), 2));
   }
   public void setDiameter (double newdiameter)   
   {
      diameter = newdiameter;
   }
   public double getDiameter ()
   {
      return diameter;
   }
   public double getVolume ()
   {      
      
      
      double volume = (4.0/3.0) * Math.PI * Math.pow((0.5 * diameter), 3);
      return volume;
   }
   public double getArea ()
   {
      double area = 4.0 * Math.PI * Math.pow((0.5 * diameter), 2);
      return area;
   }
    public String toString ()
   {
      DecimalFormat fmt = new DecimalFormat ("0.###");
   
      return "a volume of " + fmt.format(spherev) + ", and an area of " + fmt.format(spherea) + ".";
   }
}
