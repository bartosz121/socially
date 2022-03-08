import { useEffect, useState } from 'react'
import axios from 'axios'

const useFetchData = (url) => {
  const [data, setData] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async (fetchUrl) => {
      try {
        const { data: response } = await axios.get(url)
        console.log(response)
        setData(response)
      } catch (error) {
        console.error(error)
      }
      setLoading(false);
    }

    fetchData(url)
  }, [])

  return {
    data,
    loading,
  }
}

export default useFetchData;