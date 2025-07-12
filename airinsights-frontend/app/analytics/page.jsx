'use client'
import { useState, useEffect } from 'react'
import axios from 'axios'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import {
  AnalyticsBarChart,
  AnalyticsPieChart,
  AnalyticsLineChart,
  AnalyticsMultiBarChart,
  SummaryCard,
  ChartLoading,
  ChartError
} from '@/components/ui/charts'

export default function AnalyticsDashboard() {
  const [dashboardData, setDashboardData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get(`${process.env.NEXT_PUBLIC_BACKEND_URL}/flights/dashboard`)
      
      // Validate response data
      if (!response.data) {
        throw new Error('No data received from server')
      }
      
      console.log('Analytics data received:', response.data)
      setDashboardData(response.data)
    } catch (err) {
      console.error('Analytics fetch error:', err)
      setError(err.response?.data?.error || err.message || 'Failed to fetch dashboard data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDashboardData()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto py-8 px-4">
          <ChartLoading message="Loading real-time analytics dashboard..." />
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto py-8 px-4">
          <div className="max-w-2xl mx-auto">
            <ChartError 
              message={`${error}. Please ensure the backend server is running on ${process.env.NEXT_PUBLIC_BACKEND_URL} and AviationStack API is configured.`} 
              onRetry={fetchDashboardData} 
            />
          </div>
        </div>
      </div>
    )
  }

  if (!dashboardData) {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto py-8 px-4">
          <ChartError message="No real-time data available" onRetry={fetchDashboardData} />
        </div>
      </div>
    )
  }

  const { flight_overview, trend_analysis, dashboard_summary } = dashboardData || {}

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-7xl mx-auto space-y-8">
      
          <div className="text-center space-y-4">
            <h1 className="text-4xl font-bold tracking-tight">Real-Time Analytics Dashboard</h1>
            <p className="text-xl text-muted-foreground">
              Live flight analytics and market insights from AviationStack API
            </p>
            {dashboard_summary?.last_updated && (
              <p className="text-sm text-muted-foreground">
                Last updated: {new Date(dashboard_summary.last_updated).toLocaleString('en-IN', {
                  year: 'numeric',
                  month: 'short',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit',
                  second: '2-digit',
                  hour12: true,
                  timeZone: 'Asia/Kolkata'
                })}
              </p>
            )}
            {dashboard_summary?.data_source && (
              <p className="text-xs text-muted-foreground">
                Data source: {dashboard_summary.data_source}
              </p>
            )}
          </div>

      
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <SummaryCard
              title="Active Flights"
              value={dashboard_summary?.total_active_flights || 0}
              subtitle="Currently tracked"
              icon="✈️"
            />
            <SummaryCard
              title="Unique Routes"
              value={dashboard_summary?.unique_routes || 0}
              subtitle="Active routes"
              icon="🛣️"
            />
            <SummaryCard
              title="Active Airports"
              value={dashboard_summary?.active_airports || 0}
              subtitle="Airports with activity"
              icon="🏢"
            />
            <SummaryCard
              title="Last Updated"
              value={dashboard_summary?.last_updated ? new Date(dashboard_summary.last_updated).toLocaleTimeString('en-IN', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: true,
                timeZone: 'Asia/Kolkata'
              }) : 'N/A'}
              subtitle="Data freshness"
              icon="🕒"
            />
          </div>

      
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-3xl font-bold tracking-tight">Flight Overview</h2>
              <p className="text-muted-foreground mt-2">
                Real-time flight status and airport activity from AviationStack
              </p>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
              <AnalyticsPieChart
                data={flight_overview?.status || []}
                title="Flight Status Distribution"
                height={300}
              />
              
          
              <AnalyticsBarChart
                data={flight_overview?.airports?.origin || []}
                title="Top Origin Airports"
                xKey="name"
                yKey="value"
                height={300}
              />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
              <AnalyticsBarChart
                data={flight_overview?.airports?.destination || []}
                title="Top Destination Airports"
                xKey="name"
                yKey="value"
                height={300}
              />
              
          
              <AnalyticsBarChart
                data={trend_analysis?.airlines?.top_performers?.slice(0, 5) || []}
                title="Top Airlines"
                xKey="name"
                yKey="market_share"
                height={300}
              />
            </div>
          </div>

      
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-3xl font-bold tracking-tight">Market Trends & Analysis</h2>
              <p className="text-muted-foreground mt-2">
                Popular routes, airline performance, and market insights from real flight data
              </p>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
              <AnalyticsBarChart
                data={trend_analysis?.routes?.popular || []}
                title="Popular Routes"
                xKey="name"
                yKey="frequency"
                height={300}
              />
              
          
              <AnalyticsBarChart
                data={trend_analysis?.airports?.high_demand || []}
                title="High Demand Airports"
                xKey="name"
                yKey="total_flights"
                height={300}
              />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
              <AnalyticsBarChart
                data={trend_analysis?.airlines?.top_performers || []}
                title="Top Airlines by Market Share"
                xKey="name"
                yKey="market_share"
                height={300}
              />
              
          
              <AnalyticsMultiBarChart
                data={trend_analysis?.airports?.high_demand?.slice(0, 8) || []}
                title="Airport Activity (Departures vs Arrivals)"
                xKey="name"
                yKeys={["departures", "arrivals"]}
                height={300}
              />
            </div>

        
            {trend_analysis?.time_analysis?.peak_hours && trend_analysis.time_analysis.peak_hours.length > 0 && (
              <div className="grid grid-cols-1 gap-6">
                <AnalyticsLineChart
                  data={trend_analysis.time_analysis.peak_hours}
                  title="Peak Departure Hours"
                  xKey="time"
                  yKey="flights"
                  height={300}
                />
              </div>
            )}
          </div>

      
          <div className="flex justify-center pt-8">
            <Button
              onClick={fetchDashboardData}
              size="lg"
              disabled={loading}
              className="min-w-[200px]"
            >
              {loading ? 'Refreshing...' : 'Refresh Real-Time Data'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
} 