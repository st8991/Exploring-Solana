# Created 12/12/2024
# By st8991

import asyncio
import json
import websockets

async def kraken_order_book(symbol: str = XBT/USD, depth: int = 10):
    # Kraken public websocket endpoint
    uri = wss://ws.kraken.com

    # The subscription message for the order book
    # Refer to: https://docs.kraken.com/websockets/#message-subscribe
    subscribe_msg = {
        event: subscribe,
        pair: [symbol],
        subscription: {
            name: book,
            depth: depth
        }
    }

    async with websockets.connect(uri) as ws:
        # Send subscription request
        await ws.send(json.dumps(subscribe_msg))

        # Listen for messages
        while True:
            try:
                message = await ws.recv()
                data = json.loads(message)

                # Kraken responses include a variety of messages:
                # - Heartbeat messages: { event: heartbeat }
                # - System status: { event: systemStatus, ... }
                # - Subscription status: { event: subscriptionStatus, ... }
                # - Order book updates: [channelID, { ...book data... }, book, pair ]

                # Filter out events and focus on order book updates
                # A typical order book update message:
                # [channel_id, { as: [...asks data...], bs: [...bids data...] }, book, XBT/USD]
                
                if isinstance(data, list) and len(data) > 1:
                    # This should be a data message (not an event)
                    # The data for order book updates often looks like:
                    # e.g., [42, {as:[[30000.1,1.2345678,1616661115.4567]], bs:[]}, book, XBT/USD]
                    
                    # Parse bids and asks if present
                    order_book_data = data[1]
                    if as in order_book_data:
                        new_asks = order_book_data[as]  # list of [price, volume, timestamp]
                        print(Asks Update:)
                        for ask in new_asks:
                            price, volume, update_time = ask
                            print(fPrice: {price}, Volume: {volume}, Time: {update_time})

                    if bs in order_book_data:
                        new_bids = order_book_data[bs]
                        print(Bids Update:)
                        for bid in new_bids:
                            price, volume, update_time = bid
                            print(fPrice: {price}, Volume: {volume}, Time: {update_time})

                elif isinstance(data, dict) and event in data:
                    # Handle event messages like subscriptionStatus
                    event_type = data.get(event)
                    if event_type == subscriptionStatus:
                        status = data.get(status, unknown)
                        print(fSubscription status: {status})
                    elif event_type == heartbeat:
                        print(Heartbeat received)
                    elif event_type == systemStatus:
                        print(System status:, data)

            except websockets.ConnectionClosed as e:
                print(WebSocket connection closed:, e)
                break

# Run the async main function
asyncio.run(kraken_order_book()) 
