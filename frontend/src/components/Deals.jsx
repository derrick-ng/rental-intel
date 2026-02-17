import { useState, useEffect } from "react";
import api from "../api/client";

export default function Deals() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [showOverallBestValue, setShowOverallBestValue] = useState(false);
  const [showBelowMarket, setShowBelowMarket] = useState(false);
  const [showBestPricePerSqft, setShowBestPricePerSqft] = useState(false);

  useEffect(() => {
    fetchDeals();
  }, []);

  const fetchDeals = async () => {
    try {
      const response = await api.get("/listings/analytics/");
      setData(response.data);
    } catch (err) {
      console.error("Error fetching deals", err);
      setError(err.message || "Failed to fetch deals");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">Loading deals...</div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-red-600">{error ? `Error: ${error}` : "No deals data available."}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Best Deals</h1>

        {/* Overall Best Value*/}
        <div className="bg-white rounded-lg shadow-sm mb-6">
          <button
            type="button"
            onClick={() => setShowOverallBestValue((prev) => !prev)}
            className="w-full flex items-center justify-between px-6 py-4 text-left"
          >
            <span className="text-xl font-bold text-gray-900">Overall Best Value</span>
            <span className="text-gray-500 text-sm">{showOverallBestValue ? "Hide" : "Show"}</span>
          </button>

          {showOverallBestValue && (
            <div className="border-t border-gray-200 p-6">
              {data.overall_best_value?.length === 0 ? (
                <p className="text-gray-500">No listings meet the criteria yet.</p>
              ) : (
                <div className="space-y-3">
                  {data.overall_best_value?.map((deal, index) => (
                    <a key={deal.id} href={deal.url} target="_blank" rel="noreferrer">
                      <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-bold text-gray-400">#{index + 1}</span>
                              <div className="font-medium text-gray-900">{deal.title}</div>
                            </div>
                            <div className="text-sm text-gray-500 mt-1">
                              {deal.location} • {deal.bedrooms}BR / {deal.bathrooms}BA • {deal.sqft} sqft
                            </div>
                            <div className="flex gap-4 text-xs text-gray-600 mt-2">
                              <span>${deal.details.price_per_sqft}/sqft</span>
                              <span>${deal.details.price_per_bedroom}/BR</span>
                              {deal.details.percent_below_avg && <span>{deal.details.percent_below_avg}% below neighborhood avg</span>}
                            </div>
                            {(deal.parking || deal.laundry_type) && (
                              <div className="flex gap-3 text-xs text-gray-500 mt-1">
                                {deal.parking && <span>Parking: {deal.parking.replace("_", " ")}</span>}
                                {deal.laundry_type && <span>Washer/Dryer: {deal.laundry_type.replace("_", " ")}</span>}
                              </div>
                            )}
                          </div>
                          <div className="text-right ml-4">
                            <div className="text-lg font-bold text-purple-600">Score: {deal.total_score}</div>
                            <div className="text-sm text-gray-500">${deal.price.toLocaleString()}</div>
                          </div>
                        </div>
                      </div>
                    </a>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Below Market Deals */}
        <div className="bg-white rounded-lg shadow-sm mb-6">
          <button
            type="button"
            onClick={() => setShowBelowMarket((prev) => !prev)}
            className="w-full flex items-center justify-between px-6 py-4 text-left"
          >
            <span className="text-xl font-bold text-gray-900">Below Market (Priced Under Neighborhood Average)</span>
            <span className="text-gray-500 text-sm">{showBelowMarket ? "Hide" : "Show"}</span>
          </button>

          {showBelowMarket && (
            <div className="border-t border-gray-200 p-6">
              {data.good_deals?.length === 0 ? (
                <p className="text-gray-500">No deals found yet. Check back after more data is collected!</p>
              ) : (
                <div className="space-y-3">
                  {data.good_deals?.map((deal, index) => (
                    <a key={deal.id} href={deal.url} target="_blank" rel="noreferrer">
                      <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-bold text-gray-400">#{index + 1}</span>
                              <div className="font-medium text-gray-900">{deal.title}</div>
                            </div>
                            <div className="text-sm text-gray-500 mt-1">{deal.location}</div>
                          </div>
                          <div className="text-right ml-4">
                            <div className="text-lg font-bold text-green-600">${deal.price.toLocaleString()}</div>
                            <div className="text-xs text-gray-500">Avg: ${deal.avg_price.toLocaleString()}</div>
                            <div className="text-xs font-medium text-green-600">
                              Save ${deal.savings.toLocaleString()} ({deal.savings_percent}%)
                            </div>
                          </div>
                        </div>
                      </div>
                    </a>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Best Price Per Sqft */}
        <div className="bg-white rounded-lg shadow-sm mb-6">
          <button
            type="button"
            onClick={() => setShowBestPricePerSqft((prev) => !prev)}
            className="w-full flex items-center justify-between px-6 py-4 text-left"
          >
            <span className="text-xl font-bold text-gray-900">Best Price Per Square Foot</span>
            <span className="text-gray-500 text-sm">{showBestPricePerSqft ? "Hide" : "Show"}</span>
          </button>

          {showBestPricePerSqft && (
            <div className="border-t border-gray-200 p-6">
              {data.best_price_per_sqft?.length === 0 ? (
                <p className="text-gray-500">No listings with square footage data available.</p>
              ) : (
                <div className="space-y-3">
                  {data.best_price_per_sqft?.map((deal, index) => (
                    <a key={deal.id} href={deal.url} target="_blank" rel="noreferrer">
                      <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-bold text-gray-400">#{index + 1}</span>
                              <div className="font-medium text-gray-900">{deal.title}</div>
                            </div>
                            <div className="text-sm text-gray-500 mt-1">
                              {deal.location} • {deal.bedrooms}BR / {deal.bathrooms}BA
                            </div>
                            <div className="text-sm text-gray-600 mt-1">{deal.sqft} sqft</div>
                          </div>
                          <div className="text-right ml-4">
                            <div className="text-lg font-bold text-blue-600">${deal.price_per_sqft}/sqft</div>
                            <div className="text-sm text-gray-500">${deal.price.toLocaleString()} total</div>
                          </div>
                        </div>
                      </div>
                    </a>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
