import React from 'react'
import graphql2chartjs from 'graphql2chartjs'
import Client from 'apollo-boost'
import { useQuery, ApolloProvider } from 'react-apollo'
import { Box } from 'hybrid-components'
import { Line } from 'react-chartjs-2'
import gql from 'graphql-tag'

const URI = 'http://localhost:8090/'

const QUERY = gql`
    {
        eventWindows(cursorField: timestamp) {
            eventWindows: nodes {
                label: timestamp
                data: count
            }
        }
    }
`

const App: React.FC = () => {
    const g2c = new graphql2chartjs()
    const { data, loading } = useQuery(QUERY)
    if (loading) {
        return <div>loading...</div>
    }
    console.log(data)
    // add graphql data to graphql2chartjs instance while adding different chart types and properties
    g2c.add(data.eventWindows, (dataSetName, dataPoint) => {
        console.log(dataPoint)
        return {
            ...dataPoint,
            chartType: 'line',
            borderColor: '#333538',
            pointBackgroundColor: '#333538',
            backgroundColor: '#333538',
            fill: false
        }
    })
    console.log(g2c.data)
    return (
        <Box>
            <Line
                data={g2c.data}
                options={{
                  scales: {
                    xAxes: [{
                        gridLines: {
                            display:false
                        }
                    }],
                    yAxes: [{
                        gridLines: {
                            display:false
                        }   
                    }]
                }
                }}
            />
        </Box>
    )
}

const client = new Client({ uri: URI })

export default () => {
    return (
        <ApolloProvider client={client}>
            <App />
        </ApolloProvider>
    )
}
