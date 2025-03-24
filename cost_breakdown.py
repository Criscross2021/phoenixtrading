from trytond.pool import Pool
from trytond.transaction import Transaction

class CostBreakdown:
    def __init__(self, trade):
        """
        Initialize the CostBreakdown class.

        Args:
            trade (CommodityTrade): An instance of the CommodityTrade class.
        """
        self.trade = trade

    def calculate_total_cost(self, quantity, unit, commodity, trade_term, cost_params):
        """
        Calculate the total cost for the given quantity of the selected commodity and trade term.

        Args:
            quantity (float): The quantity of the commodity.
            unit (str): The unit of measurement (e.g., "tonnes").
            commodity (str): The selected commodity (e.g., "soybeans").
            trade_term (str): The selected trade term (e.g., "FOB Storage").
            cost_params (dict): A dictionary of cost parameters.

        Returns:
            dict: A dictionary containing the cost breakdown.
        """
        try:
            # Convert quantity to tonnes
            quantity_tonnes = self.trade.convert_to_tonnes(quantity, unit, commodity)

            # Calculate costs
            purchase_price = quantity_tonnes * cost_params.get("purchase_price_per_unit", 0)
            processing_fee = quantity_tonnes * cost_params.get("processing_fee_per_unit", 0)
            trucking_farm_to_storage = quantity_tonnes * cost_params.get("trucking_farm_to_storage_per_unit", 0)
            storage_fee = quantity_tonnes * cost_params.get("storage_fee_per_unit", 0)
            loading_containers_rls = cost_params.get("loading_containers_rls", 0)
            trucking_storage_to_port = quantity_tonnes * cost_params.get("trucking_storage_to_port_per_unit", 0)
            truck_free_time_hours = cost_params.get("truck_free_time_hours", 0)
            truck_free_time_rls = cost_params.get("truck_free_time_rls", 0)
            empty_containers = cost_params.get("empty_containers", 0)
            truck_unloading_rls = cost_params.get("truck_unloading_rls", 0)
            terminal_free_time_days = cost_params.get("terminal_free_time_days", 0)
            storage_fee_port = quantity_tonnes * cost_params.get("storage_fee_port_per_unit", 0)
            port_handling_fee = quantity_tonnes * cost_params.get("port_handling_per_unit", 0)
            ad_valorem = cost_params.get("ad_valorem", 0)
            ICMS_unit = cost_params.get("ICMS_unit", 0)
            ocean_freight = quantity_tonnes * cost_params.get("ocean_freight_per_tonne", 0)
            carrier_security_fee = quantity_tonnes * cost_params.get("carrier_security_fee_per_tonne", 0)
            bunker_recovery_charge = quantity_tonnes * cost_params.get("bunker_recovery_charge_per_tonne", 0)
            pilotage_service_cost = quantity_tonnes * cost_params.get("pilotage_service_cost_per_tonne", 0)
            demurrage_load = cost_params.get("demurrage_load_per_day", 0) * cost_params.get("demurrage_load_days", 0)
            detention_load = cost_params.get("detention_load_per_day", 0) * cost_params.get("detention_load_days", 0)
            ship_owner_free_time_days = cost_params.get("ship_owner_free_time_days", 0)
            terminal_handling_charge_load = quantity_tonnes * cost_params.get("terminal_handling_charge_load_per_tonne", 0)
            ship_port_security = quantity_tonnes * cost_params.get("ship_port_security_per_tonne", 0)
            documentation_fee = cost_params.get("documentation_fee", 0)
            seal_fee = cost_params.get("seal_fee", 0)
            insurance_cost = quantity_tonnes * cost_params.get("insurance_per_tonne", 0) if trade_term == "CIF" else 0
            destination_port_fee = quantity_tonnes * cost_params.get("terminal_handling_charge_disport_per_tonne", 0)
            delivery_order_fee = cost_params.get("delivery_order_fee", 0)
            inland_transport_destination = quantity_tonnes * cost_params.get("inland_transport_destination_per_tonne", 0)
            storage_fee_destination = quantity_tonnes * cost_params.get("storage_fee_destination_per_tonne", 0)
            detention_discharge_days = cost_params.get("detention_discharge_days", 0) * cost_params.get("detention_per_day_load", 0)

            # Additional costs from additional_costs_frame.py
            profit_sharing = cost_params.get("profit_sharing", 0)
            profit_sharing_brl_per_sack = cost_params.get("profit_sharing_brl_per_sack", 0)
            commodity_trader_commission = cost_params.get("commodity_trader_commission", 0)
            ship_broker_commission = cost_params.get("ship_broker_commission", 0)

            # Sum up all costs
            total_cost_usd = (
                purchase_price
                + processing_fee
                + trucking_farm_to_storage
                + storage_fee
                + loading_containers_rls
                + trucking_storage_to_port
                + truck_free_time_hours
                + truck_free_time_rls
                + empty_containers
                + truck_unloading_rls
                + terminal_free_time_days
                + storage_fee_port
                + port_handling_fee
                + ad_valorem
                + ICMS_unit
                + ocean_freight
                + carrier_security_fee
                + bunker_recovery_charge
                + pilotage_service_cost
                + demurrage_load
                + detention_load
                + ship_owner_free_time_days
                + terminal_handling_charge_load
                + ship_port_security
                + documentation_fee
                + seal_fee
                + insurance_cost
                + destination_port_fee
                + delivery_order_fee
                + inland_transport_destination
                + storage_fee_destination
                + detention_discharge_days
                + profit_sharing
                + commodity_trader_commission
                + ship_broker_commission
            )

            # Calculate total cost per metric tonne
            total_cost_per_tonne = total_cost_usd / quantity_tonnes

            # Convert total cost to BRL, EUR, and CNY
            total_cost_brl = self.trade.convert_usd_to_brl(total_cost_usd)
            total_cost_eur = self.trade.convert_usd_to_eur(total_cost_usd)
            total_cost_yuan = self.trade.convert_usd_to_yuan(total_cost_usd)

            # Save cost breakdown to Tryton database
            with Transaction().start('database_name', 0, readonly=False) as transaction:
                CostBreakdown = Pool().get('comerciointl_module.cost_breakdown')
                cost_breakdown = CostBreakdown(
                    sale=self.sale,
                    cost_component="Total Cost",
                    amount=total_cost_usd,
                    currency="USD",
                )
                cost_breakdown.save()
                transaction.commit()

            # Return cost breakdown
            return {
                "Purchase Price": purchase_price,
                "Processing Fee": processing_fee,
                "Trucking (Farm to Storage)": trucking_farm_to_storage,
                "Storage Fee": storage_fee,
                "Loading Containers (RLS)": loading_containers_rls,
                "Trucking (Storage to Port)": trucking_storage_to_port,
                "Truck Free Time (Hours)": truck_free_time_hours,
                "Truck Free Time (RLS)": truck_free_time_rls,
                "Empty Containers": empty_containers,
                "Truck Unloading (RLS)": truck_unloading_rls,
                "Terminal Free Time (Days)": terminal_free_time_days,
                "Storage Fee (Port)": storage_fee_port,
                "Port Handling Fee": port_handling_fee,
                "Ad Valorem": ad_valorem,
                "ICMS": ICMS_unit,
                "Ocean Freight": ocean_freight,
                "Carrier Security Fee": carrier_security_fee,
                "Bunker Recovery Charge": bunker_recovery_charge,
                "Pilotage Service Cost": pilotage_service_cost,
                "Demurrage (Load)": demurrage_load,
                "Detention (Load)": detention_load,
                "Ship Owner Free Time (Days)": ship_owner_free_time_days,
                "Terminal Handling Charge (Load)": terminal_handling_charge_load,
                "Ship and Port Security": ship_port_security,
                "Documentation Fee": documentation_fee,
                "Seal Fee": seal_fee,
                "Insurance": insurance_cost,
                "Destination Port Fee": destination_port_fee,
                "Delivery Order Fee": delivery_order_fee,
                "Inland Transport (Destination)": inland_transport_destination,
                "Storage Fee at Destination": storage_fee_destination,
                "Detention at Destination": detention_discharge_days,
                "Profit Sharing (USD/MT)": profit_sharing,
                "Profit Sharing (BRL/Sack)": profit_sharing_brl_per_sack,
                "Commodity Trader Commission (USD/MT)": commodity_trader_commission,
                "Ship Broker Commission (USD)": ship_broker_commission,
                "Total Cost (USD)": total_cost_usd,
                "Total Cost (BRL)": total_cost_brl,
                "Total Cost (EUR)": total_cost_eur,
                "Total Cost (CNY)": total_cost_yuan,
                "Total Cost per Tonne (USD)": total_cost_per_tonne,
            }
        except Exception as e:
            print(f"Error calculating total cost: {e}")
            return {}