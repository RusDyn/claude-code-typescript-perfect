# Complete Dashboard Example

Full implementation of a modern, professional dashboard following all design principles.

## Dashboard.jsx

```jsx
export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-8">
              <h1 className="text-xl font-bold text-gray-900">Dashboard</h1>
              <nav className="hidden md:flex gap-6">
                <a
                  href="#"
                  className="text-gray-700 hover:text-gray-900 font-medium"
                >
                  Overview
                </a>
                <a href="#" className="text-gray-600 hover:text-gray-900">
                  Analytics
                </a>
                <a href="#" className="text-gray-600 hover:text-gray-900">
                  Reports
                </a>
              </nav>
            </div>

            <div className="flex items-center gap-4">
              <button className="p-2 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100">
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                  />
                </svg>
              </button>

              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-sm font-medium text-white">JD</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, John
          </h2>
          <p className="text-base text-gray-600">
            Here's what's happening with your account today.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Stat Card 1 */}
          <div className="bg-white p-6 border border-gray-200 rounded-lg">
            <p className="text-sm font-medium text-gray-600 mb-2">
              Total Revenue
            </p>
            <p className="text-3xl font-bold text-gray-900 mb-2">$45,231</p>
            <p className="text-sm text-green-700 flex items-center gap-1">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z"
                  clipRule="evenodd"
                />
              </svg>
              +20.1% from last month
            </p>
          </div>

          {/* Stat Card 2 */}
          <div className="bg-white p-6 border border-gray-200 rounded-lg">
            <p className="text-sm font-medium text-gray-600 mb-2">
              New Customers
            </p>
            <p className="text-3xl font-bold text-gray-900 mb-2">+2,350</p>
            <p className="text-sm text-green-700 flex items-center gap-1">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z"
                  clipRule="evenodd"
                />
              </svg>
              +180.1% from last month
            </p>
          </div>

          {/* Stat Card 3 */}
          <div className="bg-white p-6 border border-gray-200 rounded-lg">
            <p className="text-sm font-medium text-gray-600 mb-2">
              Active Users
            </p>
            <p className="text-3xl font-bold text-gray-900 mb-2">12,234</p>
            <p className="text-sm text-gray-600">+19% from last month</p>
          </div>

          {/* Stat Card 4 */}
          <div className="bg-white p-6 border border-gray-200 rounded-lg">
            <p className="text-sm font-medium text-gray-600 mb-2">
              Conversion Rate
            </p>
            <p className="text-3xl font-bold text-gray-900 mb-2">3.24%</p>
            <p className="text-sm text-red-700 flex items-center gap-1">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M12 13a1 1 0 100 2h5a1 1 0 001-1V9a1 1 0 10-2 0v2.586l-4.293-4.293a1 1 0 00-1.414 0L8 9.586 3.707 5.293a1 1 0 00-1.414 1.414l5 5a1 1 0 001.414 0L11 9.414 14.586 13H12z"
                  clipRule="evenodd"
                />
              </svg>
              -4.3% from last month
            </p>
          </div>
        </div>

        {/* Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Chart */}
          <div className="lg:col-span-2">
            <div className="bg-white border border-gray-200 rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">
                  Revenue Overview
                </h3>
              </div>
              <div className="p-6">
                <div className="h-64 flex items-center justify-center text-gray-500">
                  {/* Chart would go here */}
                  Chart Placeholder
                </div>
              </div>
            </div>

            {/* Recent Transactions */}
            <div className="mt-8 bg-white border border-gray-200 rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">
                  Recent Transactions
                </h3>
              </div>
              <div className="divide-y divide-gray-200">
                {[1, 2, 3, 4].map(item => (
                  <div
                    key={item}
                    className="px-6 py-4 flex items-center justify-between"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                        <svg
                          className="w-5 h-5 text-gray-600"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
                          />
                        </svg>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          Payment from ABC Corp
                        </p>
                        <p className="text-sm text-gray-600">2 hours ago</p>
                      </div>
                    </div>
                    <p className="text-base font-semibold text-gray-900">
                      +$2,500
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-8">
            {/* Quick Actions */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Quick Actions
              </h3>
              <div className="space-y-3">
                <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  Create Invoice
                </button>
                <button className="w-full px-4 py-2 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200 transition-colors">
                  Add Customer
                </button>
                <button className="w-full px-4 py-2 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200 transition-colors">
                  View Reports
                </button>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Recent Activity
              </h3>
              <div className="space-y-4">
                {[1, 2, 3].map(item => (
                  <div key={item} className="flex gap-3">
                    <div className="flex-shrink-0 w-2 h-2 bg-blue-600 rounded-full mt-2" />
                    <div>
                      <p className="text-sm text-gray-900">
                        New customer registered
                      </p>
                      <p className="text-xs text-gray-600">5 minutes ago</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Notifications */}
            <div className="bg-blue-50 border-l-4 border-blue-500 rounded-r-lg p-4">
              <div className="flex gap-3">
                <svg
                  className="w-5 h-5 text-blue-500 flex-shrink-0"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clipRule="evenodd"
                  />
                </svg>
                <div>
                  <p className="text-sm font-medium text-blue-900">
                    System Update
                  </p>
                  <p className="text-sm text-blue-700 mt-1">
                    New features are now available in your dashboard.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
```

## Key Design Elements Used

1. **Colors:**
   - Gray scale for everything except actions
   - Single accent (blue-600) for primary actions
   - Semantic colors for success/error indicators

2. **Typography:**
   - Clear hierarchy (3xl → 2xl → xl → lg → base → sm)
   - Minimum 16px for body text
   - Bold headings, medium for labels

3. **Spacing:**
   - 8px grid throughout (8, 16, 24, 32, 48, 64)
   - Consistent padding (p-6 for cards)
   - Generous margins between sections

4. **Components:**
   - Subtle shadows (shadow-sm)
   - Clean borders (border-gray-200)
   - Rounded corners (rounded-lg)
   - Clear hover states

5. **Layout:**
   - Mobile-first responsive
   - Max-width containers
   - Grid system for cards
   - Sticky header

This example demonstrates all design principles in action.
