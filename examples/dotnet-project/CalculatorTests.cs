using Xunit;

namespace GoalExample.Tests;

public class CalculatorTests
{
    private readonly Calculator _calc = new();

    [Fact]
    public void Add_ReturnsSum()
    {
        Assert.Equal(5, _calc.Add(2, 3));
    }

    [Fact]
    public void Subtract_ReturnsDifference()
    {
        Assert.Equal(1, _calc.Subtract(3, 2));
    }

    [Fact]
    public void Multiply_ReturnsProduct()
    {
        Assert.Equal(6, _calc.Multiply(2, 3));
    }

    [Fact]
    public void Divide_ReturnsQuotient()
    {
        Assert.Equal(2.5, _calc.Divide(5, 2));
    }
}
