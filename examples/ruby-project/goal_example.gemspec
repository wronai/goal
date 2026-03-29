Gem::Specification.new do |spec|
  spec.name          = "goal_example"
  spec.version       = GoalExample::VERSION
  spec.authors       = ["Your Name"]
  spec.email         = ["you@example.com"]
  spec.summary       = "Example Ruby project with Goal"
  spec.description   = "A longer description of the project"
  spec.homepage      = "https://github.com/example/goal_example"
  spec.license       = "MIT"
  
  spec.files         = Dir["lib/**/*"]
  spec.require_paths = ["lib"]
  
  spec.add_development_dependency "rspec", "~> 3.0"
  spec.add_development_dependency "goal", "~> 2.0"
end
