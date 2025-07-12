'use client'
import { useState } from 'react'
import axios from 'axios'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { useRef } from 'react'

export default function Dashboard() {
  const [flights, setFlights] = useState([])
  const [scrapedFlights, setScrapedFlights] = useState([])
  const [insights, setInsights] = useState('')
  const [loading, setLoading] = useState({ flights: false, scraped: false, insights: false })
  const [errors, setErrors] = useState({ flights: '', scraped: '', insights: '' })
  const insightsRef = useRef(null)

  const fetchFlights = async () => {
    setLoading(prev => ({ ...prev, flights: true }))
    setErrors(prev => ({ ...prev, flights: '' }))
    try {
      const res = await axios.get(`${process.env.NEXT_PUBLIC_BACKEND_URL}/flights`)
      setFlights(res.data)
    } catch (error) {
      console.error('Failed to fetch flights:', error)
      setErrors(prev => ({ 
        ...prev, 
        flights: error.response?.data?.error || 'Failed to fetch scheduled flights. Please check if the backend server is running.' 
      }))
    } finally {
      setLoading(prev => ({ ...prev, flights: false }))
    }
  }

  const fetchScraped = async () => {
    setLoading(prev => ({ ...prev, scraped: true }))
    setErrors(prev => ({ ...prev, scraped: '' }))
    try {
      const res = await axios.get(`${process.env.NEXT_PUBLIC_BACKEND_URL}/scraped`)
      setScrapedFlights(res.data)
    } catch (error) {
      console.error('Failed to fetch scraped data:', error)
      setErrors(prev => ({ 
        ...prev, 
        scraped: error.response?.data?.error || 'Failed to fetch live aircraft data. This may be due to API rate limits or network issues.' 
      }))
    } finally {
      setLoading(prev => ({ ...prev, scraped: false }))
    }
  }

  const generateInsights = async () => {
    setLoading(prev => ({ ...prev, insights: true }))
    setErrors(prev => ({ ...prev, insights: '' }))
    try {
      const combinedData = [...flights, ...scrapedFlights]
      if (combinedData.length === 0) {
        setInsights('No data available for analysis. Please fetch some flight data first.')
        return
      }
      
      const res = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/insights`, combinedData)
      setInsights(res.data.insights)
      
    
      setTimeout(() => {
        if (insightsRef.current) {
          insightsRef.current.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start',
            inline: 'nearest'
          })
        }
      }, 100)
      
    } catch (error) {
      console.error('Failed to generate insights:', error)
      setErrors(prev => ({ 
        ...prev, 
        insights: error.response?.data?.error || 'Failed to generate insights. Please try again.' 
      }))
      setInsights('Failed to generate insights. Please check your connection and try again.')
    } finally {
      setLoading(prev => ({ ...prev, insights: false }))
    }
  }

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold">AirInsights Dashboard</h1>
          <p className="text-muted-foreground">Real-time flight data and analytics</p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-4 justify-center">
          <Button 
            onClick={fetchFlights}
            disabled={loading.flights}
            className="min-w-[150px]"
          >
            {loading.flights ? 'Loading...' : 'Get Scheduled Flights'}
          </Button>
          
          <Button 
            onClick={fetchScraped}
            disabled={loading.scraped}
            className="min-w-[150px]"
          >
            {loading.scraped ? 'Loading...' : 'Get Live Aircraft'}
          </Button>
          
          <Button 
            onClick={generateInsights}
            disabled={loading.insights || (flights.length === 0 && scrapedFlights.length === 0)}
            variant="outline"
            className="min-w-[150px]"
          >
            {loading.insights ? 'Generating...' : 'Generate Insights'}
          </Button>
        </div>

        {/* Error Messages */}
        {(errors.flights || errors.scraped || errors.insights) && (
          <div className="space-y-2">
            {errors.flights && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
                <strong>Scheduled Flights Error:</strong> {errors.flights}
              </div>
            )}
            {errors.scraped && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
                <strong>Live Aircraft Error:</strong> {errors.scraped}
              </div>
            )}
            {errors.insights && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
                <strong>Insights Error:</strong> {errors.insights}
              </div>
            )}
          </div>
        )}

        {/* Data Display */}
        <div className="grid md:grid-cols-2 gap-8">
          {/* Scheduled Flights */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <span className="text-2xl">✈️</span>
                Scheduled Flights
              </CardTitle>
            </CardHeader>
            <CardContent>
              {loading.flights ? (
                <div className="text-center text-muted-foreground py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
                  Loading scheduled flights...
                </div>
              ) : flights.length === 0 ? (
                <div className="text-center text-muted-foreground py-8">No scheduled flights. Click "Get Scheduled Flights".</div>
              ) : (
                <div className="space-y-4">
                  <div className="text-sm text-muted-foreground">
                    Showing {flights.length} flights
                  </div>
                  <div className="max-h-80 overflow-y-auto">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Flight</TableHead>
                          <TableHead>Route</TableHead>
                          <TableHead>Status</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {flights.slice(0, 10).map((flight, i) => (
                          <TableRow key={i}>
                            <TableCell className="font-medium">
                              {flight.flight_number || 'N/A'}
                            </TableCell>
                            <TableCell>
                              {flight.departure_airport} → {flight.arrival_airport}
                            </TableCell>
                            <TableCell>
                              <Badge variant={flight.status === 'active' ? 'default' : 'secondary'}>
                                {flight.status || 'Unknown'}
                              </Badge>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Live Aircraft */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <span className="text-2xl">📍</span>
                Live Aircraft
              </CardTitle>
            </CardHeader>
            <CardContent>
              {loading.scraped ? (
                <div className="text-center text-muted-foreground py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
                  Loading live traffic...
                </div>
              ) : scrapedFlights.length === 0 ? (
                <div className="text-center text-muted-foreground py-8">No live traffic data. Click "Get Live Aircraft".</div>
              ) : (
                <div className="space-y-4">
                  <div className="text-sm text-muted-foreground">
                    Showing {scrapedFlights.length} aircraft
                  </div>
                  <div className="max-h-80 overflow-y-auto">
                    <div className="grid gap-3">
                      {scrapedFlights.slice(0, 15).map((plane, i) => (
                        <div key={i} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                          <div className="flex items-center space-x-3">
                            <span className="text-muted-foreground">✈️</span>
                            <div>
                              <div className="font-medium">{plane.callsign || plane.icao24}</div>
                              <div className="text-sm text-muted-foreground">
                                {plane.origin_airport || 'Unknown'} → {plane.destination_airport || 'Unknown'}
                              </div>
                            </div>
                          </div>
                          <div className="text-right text-sm text-muted-foreground">
                            <div>{plane.origin_country || 'Unknown'}</div>
                            <div>{plane.latitude?.toFixed(2)}, {plane.longitude?.toFixed(2)}</div>
                            <div className="text-xs">
                              {plane.on_ground ? '🛬 Grounded' : '✈️ Airborne'}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Flight Statistics */}
        {(flights.length > 0 || scrapedFlights.length > 0) && (
          <div className="grid md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-6">
                <div className="text-2xl font-bold">{flights.length}</div>
                <div className="text-sm text-muted-foreground">Scheduled Flights</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6">
                <div className="text-2xl font-bold">{scrapedFlights.length}</div>
                <div className="text-sm text-muted-foreground">Live Aircraft</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6">
                <div className="text-2xl font-bold">
                  {scrapedFlights.filter(f => !f.on_ground).length}
                </div>
                <div className="text-sm text-muted-foreground">Airborne</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6">
                <div className="text-2xl font-bold">
                  {scrapedFlights.filter(f => f.on_ground).length}
                </div>
                <div className="text-sm text-muted-foreground">Grounded</div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Insights Section */}
        {insights && (
          <Card ref={insightsRef} className="border-2 border-blue-200 bg-blue-50/30">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <span className="text-2xl">💡</span>
                AI Insights
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="prose prose-sm max-w-none">
                <p className="whitespace-pre-wrap text-sm leading-relaxed">{insights}</p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Data Source Information */}
        <Card className="bg-muted/30">
          <CardContent className="p-6">
            <div className="text-center space-y-2">
              <h3 className="font-semibold">Data Sources</h3>
              <div className="text-sm text-muted-foreground space-y-1">
                <div>• Scheduled Flights: AviationStack API</div>
                <div>• Live Aircraft: FlightRadar24, OpenSky Network</div>
                <div>• AI Insights: Google Gemini AI</div>
              </div>
              <div className="text-xs text-muted-foreground mt-4">
                Last updated: {new Date().toLocaleString()}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}