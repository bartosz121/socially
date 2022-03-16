import { useEffect, useState } from 'react'
import axios from 'axios'

const useFetchData = (url) => {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)

      try {
        const response = await axios.get(url);
        setData(response.data)
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    }

    fetchData()
  }, [url])

  return { data, loading, error };
}

export default useFetchData;