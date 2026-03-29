// .NET Example for Goal
// This demonstrates a typical .NET project structure

namespace GoalExample;

public class Calculator
{
    public int Add(int a, int b) => a + b;
    public int Subtract(int a, int b) => a - b;
    public int Multiply(int a, int b) => a * b;
    public double Divide(int a, int b) => b == 0 ? throw new DivideByZeroException() : (double)a / b;
}

public class Program
{
    public static void Main(string[] args)
    {
        var calc = new Calculator();
        Console.WriteLine($"2 + 3 = {calc.Add(2, 3)}");
    }
}
