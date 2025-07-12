import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto py-16 px-4">
        <div className="max-w-6xl mx-auto space-y-16">
          {/* Hero Section */}
          <div className="text-center space-y-8">
            <div className="space-y-4">
              <h1 className="text-6xl font-bold tracking-tight">
                AirInsights
              </h1>
              <p className="text-2xl text-muted-foreground max-w-3xl mx-auto">
                Real-time airline demand analysis and market insights powered by AI
              </p>
            </div>
            
            <div className="flex flex-wrap justify-center gap-4">
              <Button asChild size="lg">
                <a href="/dashboard">Get Started</a>
              </Button>
              <Button asChild size="lg" variant="outline">
                <a href="/analytics">View Analytics</a>
              </Button>
            </div>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="text-center">
              <CardHeader>
                <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">✈️</span>
                </div>
                <CardTitle>Live Flight Data</CardTitle>
                <CardDescription>
                  Real-time flight tracking and status monitoring with comprehensive data from multiple sources
                </CardDescription>
              </CardHeader>
            </Card>
            
            <Card className="text-center">
              <CardHeader>
                <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">📊</span>
                </div>
                <CardTitle>Market Analytics</CardTitle>
                <CardDescription>
                  Advanced demand trends, route analysis, and competitive market insights
                </CardDescription>
              </CardHeader>
            </Card>
            
            <Card className="text-center">
              <CardHeader>
                <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🤖</span>
                </div>
                <CardTitle>AI Insights</CardTitle>
                <CardDescription>
                  Intelligent analysis powered by AI to uncover hidden patterns and opportunities
                </CardDescription>
              </CardHeader>
            </Card>
          </div>

          {/* Stats Section */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <Card>
              <CardContent className="p-6 text-center">
                <div className="text-3xl font-bold text-primary">100+</div>
                <div className="text-sm text-muted-foreground">Active Routes</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6 text-center">
                <div className="text-3xl font-bold text-primary">50+</div>
                <div className="text-sm text-muted-foreground">Airports</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6 text-center">
                <div className="text-3xl font-bold text-primary">24/7</div>
                <div className="text-sm text-muted-foreground">Real-time Data</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6 text-center">
                <div className="text-3xl font-bold text-primary">AI</div>
                <div className="text-sm text-muted-foreground">Powered Insights</div>
              </CardContent>
            </Card>
          </div>

          {/* CTA Section */}
          <div className="text-center space-y-6">
            <div className="space-y-4">
              <h2 className="text-3xl font-bold tracking-tight">
                Ready to explore airline insights?
              </h2>
              <p className="text-lg text-muted-foreground">
                Start analyzing real-time flight data and market trends today
              </p>
            </div>
            <Button asChild size="lg">
              <a href="/dashboard">Launch Dashboard</a>
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
