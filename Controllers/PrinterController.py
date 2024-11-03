from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional, Dict, Any
from Models.Printer import Printer, PrinterSchema
from pydantic import BaseModel


class PrinterCreate(BaseModel):
    name: str
    val_print_x: Optional[float] = None
    val_print_y: Optional[float] = None
    val_print_z: Optional[float] = None
    view_table: Optional[str] = None
    center_origin: Optional[bool] = None
    table_heating: Optional[bool] = None
    print_volume_heating: Optional[bool] = None
    type_g_code: Optional[str] = None
    min_x_head: Optional[float] = None
    min_y_head: Optional[float] = None
    max_x_head: Optional[float] = None
    max_y_head: Optional[float] = None
    height_portal: Optional[float] = None
    displace_extruder: Optional[bool] = None
    count_extruder: Optional[int] = None
    start_g_code: Optional[str] = None
    end_g_code: Optional[str] = None
    extr_1_nozzle_diameter: Optional[float] = None
    extr_1_filament_diameter: Optional[float] = None
    extr_1_nozzle_displacement_x: Optional[float] = None
    extr_1_nozzle_displacement_y: Optional[float] = None
    extr_1_fan_number: Optional[int] = None
    extr_1_start_g_code: Optional[str] = None
    extr_1_end_g_code: Optional[str] = None
    extr_2_nozzle_diameter: Optional[float] = None
    extr_2_filament_diameter: Optional[float] = None
    extr_2_nozzle_displacement_x: Optional[float] = None
    extr_2_nozzle_displacement_y: Optional[float] = None
    extr_2_fan_number: Optional[int] = None
    extr_2_start_g_code: Optional[str] = None
    extr_2_end_g_code: Optional[str] = None


class PrinterController:
    @staticmethod
    async def get_printers(session: AsyncSession):
        try:
            result = await session.execute(select(Printer))
            printers = result.scalars().all()
            printer_schema = PrinterSchema(many=True)
            return {"message": "OK", "data": printer_schema.dump(printers)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_printer(session: AsyncSession, item_id: int):
        try:
            result = await session.execute(
                select(Printer).filter(Printer.id == item_id)
            )
            printer = result.scalar_one_or_none()
            if not printer:
                raise HTTPException(status_code=404, detail="Printer not found")

            printer_schema = PrinterSchema()
            return {"message": "OK", "data": printer_schema.dump(printer)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def add_printer(session: AsyncSession, printer_data: PrinterCreate):
        try:
            new_printer = Printer(
                name=printer_data.name,
                val_print_x=printer_data.val_print_x,
                val_print_y=printer_data.val_print_y,
                val_print_z=printer_data.val_print_z,
                view_table=printer_data.view_table,
                center_origin=printer_data.center_origin,
                table_heating=printer_data.table_heating,
                print_volume_heating=printer_data.print_volume_heating,
                type_g_code=printer_data.type_g_code,
                min_x_head=printer_data.min_x_head,
                min_y_head=printer_data.min_y_head,
                max_x_head=printer_data.max_x_head,
                max_y_head=printer_data.max_y_head,
                height_portal=printer_data.height_portal,
                displace_extruder=printer_data.displace_extruder,
                count_extruder=printer_data.count_extruder,
                start_g_code=printer_data.start_g_code,
                end_g_code=printer_data.end_g_code,
                extr_1_nozzle_diameter=printer_data.extr_1_nozzle_diameter,
                extr_1_filament_diameter=printer_data.extr_1_filament_diameter,
                extr_1_nozzle_displacement_x=printer_data.extr_1_nozzle_displacement_x,
                extr_1_nozzle_displacement_y=printer_data.extr_1_nozzle_displacement_y,
                extr_1_fan_number=printer_data.extr_1_fan_number,
                extr_1_start_g_code=printer_data.extr_1_start_g_code,
                extr_1_end_g_code=printer_data.extr_1_end_g_code,
                extr_2_nozzle_diameter=printer_data.extr_2_nozzle_diameter,
                extr_2_filament_diameter=printer_data.extr_2_filament_diameter,
                extr_2_nozzle_displacement_x=printer_data.extr_2_nozzle_displacement_x,
                extr_2_nozzle_displacement_y=printer_data.extr_2_nozzle_displacement_y,
                extr_2_fan_number=printer_data.extr_2_fan_number,
                extr_2_start_g_code=printer_data.extr_2_start_g_code,
                extr_2_end_g_code=printer_data.extr_2_end_g_code
            )
            session.add(new_printer)
            await session.commit()
            await session.refresh(new_printer)

            return {
                "message": "Printer added successfully",
                "printer_id": new_printer.id
            }
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def create_default_printers(session: AsyncSession):
        default_printers = [
            {
                "name": "Ender 3",
                "val_print_x": 200.0,
                "val_print_y": 200.0,
                "val_print_z": 200.0,
                "view_table": "Glass",
                "center_origin": True,
                "table_heating": False,
                "print_volume_heating": False,
                "type_g_code": "G-code",
                "min_x_head": 0.0,
                "min_y_head": 0.0,
                "max_x_head": 200.0,
                "max_y_head": 200.0,
                "height_portal": 100.0,
                "displace_extruder": False,
                "count_extruder": 1,
                "start_g_code": "Start G-code",
                "end_g_code": "End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 0.0,
                "extr_1_nozzle_displacement_y": 0.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Start G-code",
                "extr_1_end_g_code": "Extruder 1 End G-code",
                "extr_2_nozzle_diameter": None,
                "extr_2_filament_diameter": None,
                "extr_2_nozzle_displacement_x": None,
                "extr_2_nozzle_displacement_y": None,
                "extr_2_fan_number": None,
                "extr_2_start_g_code": None,
                "extr_2_end_g_code": None
            },
            {
                "name": "Creality Ender 5",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "Anycubic i3 Mega",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "Ultimaker S3",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "Prusa SL1S",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "Raise3D E2",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "MakerBot Replicator Z18",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "Wanhao Duplicator 9",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "Prusa MINI+",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "UlTi Steel 2",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "FlyingBear Ghost 5",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "Creality CR-K1C",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "Anycubic Kobra 2 Neo",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "Creality K1",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "FlyingBear Ghost 6",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "ZAV-PRO V3",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
            ,
            {
                "name": "Biqu Hurakan",
                "val_print_x": 250.0,
                "val_print_y": 250.0,
                "val_print_z": 250.0,
                "view_table": "Aluminum",
                "center_origin": False,
                "table_heating": True,
                "print_volume_heating": True,
                "type_g_code": "Custom G-code",
                "min_x_head": 10.0,
                "min_y_head": 10.0,
                "max_x_head": 240.0,
                "max_y_head": 240.0,
                "height_portal": 120.0,
                "displace_extruder": True,
                "count_extruder": 2,
                "start_g_code": "Custom Start G-code",
                "end_g_code": "Custom End G-code",
                "extr_1_nozzle_diameter": 0.4,
                "extr_1_filament_diameter": 1.75,
                "extr_1_nozzle_displacement_x": 10.0,
                "extr_1_nozzle_displacement_y": 5.0,
                "extr_1_fan_number": 1,
                "extr_1_start_g_code": "Extruder 1 Custom Start G-code",
                "extr_1_end_g_code": "Extruder 1 Custom End G-code",
                "extr_2_nozzle_diameter": 0.4,
                "extr_2_filament_diameter": 1.75,
                "extr_2_nozzle_displacement_x": -10.0,
                "extr_2_nozzle_displacement_y": -5.0,
                "extr_2_fan_number": 2,
                "extr_2_start_g_code": "Extruder 2 Custom Start G-code",
                "extr_2_end_g_code": "Extruder 2 Custom End G-code"
            }
        ]
            # Добавьте сколько угодно принтеров по умолчанию
        try:
            for printer_data in default_printers:
                new_printer = Printer(**printer_data)
                session.add(new_printer)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

