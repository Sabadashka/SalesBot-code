from telebot import types

go_back = types.InlineKeyboardButton("◀️ Назад", callback_data='go_back_btn')
# Категорії
children_world = types.InlineKeyboardButton("👶 Дитячий світ", callback_data='сhildren_world_btn')
realty = types.InlineKeyboardButton("🏠 Нерухомість", callback_data='realty_markup_btn')
vehicle = types.InlineKeyboardButton("🚗 Авто", callback_data='vehicle_markup_btn')
spare_parts_transport = types.InlineKeyboardButton("🛠️ Запчастини для транспорту", callback_data='spare_parts_markup_btn')
job = types.InlineKeyboardButton("💼 Робота", callback_data='job_markup_btn')
animals = types.InlineKeyboardButton("🐾 Тварини", callback_data='animals_markup_btn')
house_garden = types.InlineKeyboardButton("🏡 Дім і сад", callback_data='house_garden_markup_btn')
electronics = types.InlineKeyboardButton("📱 Електроніка", callback_data='electronics_markup_btn')
business_services = types.InlineKeyboardButton("🤝 Бізнес та сервіси", callback_data='business_services_markup_btn')
rent_hire = types.InlineKeyboardButton("🚀 Оренда та прокат", callback_data='rent_hire_markup_btn')
fashion_style = types.InlineKeyboardButton("👗 Мода та стиль", callback_data='fashion_style_markup_btn')
hobbies_recreation_sports = types.InlineKeyboardButton("⚽ Хобі, відпочинок і спорт", callback_data='hobbies_markup_btn')

category_markup = types.InlineKeyboardMarkup(row_width=2)
category_markup.add(children_world, realty, vehicle, spare_parts_transport, job, animals, house_garden, electronics,
                    business_services, rent_hire, fashion_style, hobbies_recreation_sports)

# Підкатегорії
# children_world
children_world_clothing = types.InlineKeyboardButton("👕 Дитячий одяг", callback_data='children_world_clothing')
children_world_footwear = types.InlineKeyboardButton("👟 Дитяче взуття", callback_data='children_world_footwear')
children_world_prams = types.InlineKeyboardButton("🛍️ Дитячі коляски", callback_data='children_world_prams')
children_world_car_seats = types.InlineKeyboardButton("👶 Дитячі автокрісла", callback_data='children_world_car_seats')
children_world_furniture = types.InlineKeyboardButton("🪑 Дитячі меблі", callback_data='children_world_furniture')
children_world_toys = types.InlineKeyboardButton("🎲 Іграшки", callback_data='children_world_toys')
children_world_transport = types.InlineKeyboardButton("🚗 Дитячий транспорт", callback_data='children_world_transport')
children_world_feeding = types.InlineKeyboardButton("🍼 Годування", callback_data='children_world_feeding')
children_world_school_supplies = types.InlineKeyboardButton("🎒 Товари для школярів", callback_data='children_world_school_supplies')
children_world_others = types.InlineKeyboardButton("🔗 Інші товари", callback_data='children_world_others')

children_world_markup = types.InlineKeyboardMarkup(row_width=2)
children_world_markup.add(children_world_clothing, children_world_footwear, children_world_prams,
                          children_world_car_seats, children_world_furniture, children_world_toys,
                          children_world_transport, children_world_feeding, children_world_school_supplies,
                          children_world_others, go_back)

# realty
realty_apartments = types.InlineKeyboardButton("🏢 Квартири", callback_data='realty_apartments')
realty_rooms = types.InlineKeyboardButton("🛌 Кімнати", callback_data='realty_rooms')
realty_houses = types.InlineKeyboardButton("🏡 Будинки", callback_data='realty_houses')
realty_short_term_rental = types.InlineKeyboardButton("🏠 Подобова оренда житла", callback_data='realty_short_term_rental')
realty_land = types.InlineKeyboardButton("🌳 Земля", callback_data='realty_land')
realty_commercial_property = types.InlineKeyboardButton("🏢 Комерційна нерухомість", callback_data='realty_commercial_property')
realty_garages_parking = types.InlineKeyboardButton("🚗 Гаражі/Парковки", callback_data='realty_garages_parking')
realty_foreign_property = types.InlineKeyboardButton("🌍 Нерухомість за кордоном", callback_data='realty_foreign_property')

realty_markup = types.InlineKeyboardMarkup(row_width=2)
realty_markup.add(realty_apartments, realty_rooms, realty_houses, realty_short_term_rental,
                  realty_land, realty_commercial_property, realty_garages_parking, realty_foreign_property, go_back)

# vehicle_cars
vehicle_cars = types.InlineKeyboardButton("🚗 Легкові автомобілі", callback_data='vehicle_cars')
vehicle_trucks = types.InlineKeyboardButton("🚚 Вантажні автомобілі", callback_data='vehicle_trucks')
vehicle_buses = types.InlineKeyboardButton("🚌 Автобуси", callback_data='vehicle_buses')
vehicle_motorcycles = types.InlineKeyboardButton("🏍️ Мотоцикли", callback_data='vehicle_motorcycles')
vehicle_special_equipment = types.InlineKeyboardButton("🚜 Спецтехніка", callback_data='vehicle_special_equipment')
vehicle_agricultural_machinery = types.InlineKeyboardButton("🚜 Сільгосптехніка", callback_data='vehicle_agricultural_machinery')
vehicle_water_transport = types.InlineKeyboardButton("🛥️ Водний транспорт", callback_data='vehicle_water_transport')
vehicle_cars_from_poland = types.InlineKeyboardButton("🚗 Автомобілі з Польщі", callback_data='vehicle_cars_from_poland')
vehicle_trailers_motorhomes = types.InlineKeyboardButton("🚐 Причепи/Будинки на колесах", callback_data='vehicle_trailers_motorhomes')
vehicle_other_transport = types.InlineKeyboardButton("🚀 Інший транспорт", callback_data='vehicle_other_transport')

vehicle_markup = types.InlineKeyboardMarkup(row_width=2)
vehicle_markup.add(vehicle_cars, vehicle_trucks, vehicle_buses, vehicle_motorcycles,
                   vehicle_special_equipment, vehicle_agricultural_machinery, vehicle_water_transport,
                   vehicle_cars_from_poland, vehicle_trailers_motorhomes, vehicle_other_transport, go_back)

# spare_parts_transport
spare_parts_auto_parts = types.InlineKeyboardButton("🚗 Автозапчастини", callback_data='spare_parts_auto_parts')
spare_parts_auto_accessories = types.InlineKeyboardButton("🛠️ Аксесуари для авто", callback_data='spare_parts_auto_accessories')
spare_parts_car_audio_multimedia = types.InlineKeyboardButton("🔊 Автозвук та мультимедіа", callback_data='spare_parts_car_audio_multimedia')
spare_parts_tires_wheels = types.InlineKeyboardButton("🚗 Шини/Диски і Колеса", callback_data='spare_parts_tires_wheels')
spare_parts_gps_dashcams = types.InlineKeyboardButton("🌐 GPS-навігатори / Відеореєстратори", callback_data='spare_parts_gps_dashcams')
spare_parts_transport_for_parts = types.InlineKeyboardButton("🚛 Транспорт на запчастини / Авторозбірка", callback_data='spare_parts_transport_for_parts')
spare_parts_motorcycle_parts = types.InlineKeyboardButton("🏍️ Мотозапчастини", callback_data='spare_parts_motorcycle_parts')
spare_parts_motorcycle_gear = types.InlineKeyboardButton("👕 Мотоекіпірування", callback_data='spare_parts_motorcycle_gear')
spare_parts_motorcycle_accessories = types.InlineKeyboardButton("🛵 Мотоаксесуари", callback_data='spare_parts_motorcycle_accessories')
spare_parts_lubricants_auto_chemicals = types.InlineKeyboardButton("🧴 Мастила та Автохімія", callback_data='spare_parts_lubricants_auto_chemicals')
spare_parts_other_vehicle_parts = types.InlineKeyboardButton("🔩 Запчастини для іншої техніки", callback_data='spare_parts_other_vehicle_parts')

spare_parts_markup = types.InlineKeyboardMarkup(row_width=2)
spare_parts_markup.add(spare_parts_auto_parts, spare_parts_auto_accessories, spare_parts_car_audio_multimedia,
                      spare_parts_tires_wheels, spare_parts_gps_dashcams, spare_parts_transport_for_parts,
                      spare_parts_motorcycle_parts, spare_parts_motorcycle_gear, spare_parts_motorcycle_accessories,
                      spare_parts_lubricants_auto_chemicals, spare_parts_other_vehicle_parts, go_back)

# job
job_retail_trade = types.InlineKeyboardButton("🛒 Роздрібна торгівля / продажі / закупка", callback_data='job_retail_trade')
job_logistics_warehouse_delivery = types.InlineKeyboardButton("🚚 Логістика / Склад / Доставка", callback_data='job_logistics_warehouse_delivery')
job_construction_finish_works = types.InlineKeyboardButton("🏗️ Будівництво / Облицювальні роботи", callback_data='job_construction_finish_works')
job_call_centers_telecommunications = types.InlineKeyboardButton("📞 Колл-центри / Телекомунікації", callback_data='job_call_centers_telecommunications')
job_administrative_staff = types.InlineKeyboardButton("📋 Адміністративний персонал", callback_data='job_administrative_staff')
job_security = types.InlineKeyboardButton("🛡️ Охорона / Безпека", callback_data='job_security')
job_cleaning_domestic_staff = types.InlineKeyboardButton("🧹 Клінінг / Домашній персонал", callback_data='job_cleaning_domestic_staff')
job_beauty_fitness_sports = types.InlineKeyboardButton("💇 Краса / Фітнес / Спорт", callback_data='job_beauty_fitness_sports')
job_education_translation = types.InlineKeyboardButton("📚 Освіта / Переклад", callback_data='job_education_translation')
job_culture_art_entertainment = types.InlineKeyboardButton("🎭 Культура / Мистецтво / Розваги", callback_data='job_culture_art_entertainment')
job_medical_pharmaceutical = types.InlineKeyboardButton("🏥 Медицина / Фармацевтика", callback_data='job_medical_pharmaceutical')
job_it_computers = types.InlineKeyboardButton("💻 IT / Комп'ютери", callback_data='job_it_computers')
job_banking_finance_insurance_law = types.InlineKeyboardButton("🏦 Банки / Фінанси / Страхування / Юриспруденція", callback_data='job_banking_finance_insurance_law')
job_real_estate = types.InlineKeyboardButton("🏠 Нерухомість", callback_data='job_real_estate')
job_advertising_design_pr = types.InlineKeyboardButton("📢 Реклама / Дизайн / PR", callback_data='job_advertising_design_pr')
job_manufacturing = types.InlineKeyboardButton("🏭 Виробництво", callback_data='job_manufacturing')
job_agriculture_forestry = types.InlineKeyboardButton("🚜 Сільське і лісове господарство", callback_data='job_agriculture_forestry')
job_part_time = types.InlineKeyboardButton("🕒 Часткова зайнятість", callback_data='job_part_time')
job_accounting = types.InlineKeyboardButton("📊 Бухгалтерія", callback_data='job_accounting')
job_hotel_restaurant_business = types.InlineKeyboardButton("🏨 Готельно-ресторанний бізнес", callback_data='job_hotel_restaurant_business')
job_other_industries = types.InlineKeyboardButton("🌐 Інші сфери занять", callback_data='job_other_industries')
job_auto_service_car_washes = types.InlineKeyboardButton("🔧 СТО / Автомийки", callback_data='job_auto_service_car_washes')
job_military_service = types.InlineKeyboardButton("🎖️ Служба в Силах оборони", callback_data='job_military_service')

job_markup = types.InlineKeyboardMarkup(row_width=2)
job_markup.add(job_retail_trade, job_logistics_warehouse_delivery, job_construction_finish_works,
                job_call_centers_telecommunications, job_administrative_staff, job_security,
                job_cleaning_domestic_staff, job_beauty_fitness_sports, job_education_translation,
                job_culture_art_entertainment, job_medical_pharmaceutical, job_it_computers,
                job_banking_finance_insurance_law, job_real_estate, job_advertising_design_pr,
                job_manufacturing, job_agriculture_forestry, job_part_time, job_accounting,
                job_hotel_restaurant_business, job_other_industries, job_auto_service_car_washes,
                job_military_service, go_back)

# animals
animals_dogs = types.InlineKeyboardButton("🐶 Собаки", callback_data='animals_dogs')
animals_cats = types.InlineKeyboardButton("🐱 Коти", callback_data='animals_cats')
animals_aquarium = types.InlineKeyboardButton("🐠 Акваріумістика", callback_data='animals_aquarium')
animals_birds = types.InlineKeyboardButton("🐦 Пташки", callback_data='animals_birds')
animals_rodents = types.InlineKeyboardButton("🐭 Гризуни", callback_data='animals_rodents')
animals_reptiles = types.InlineKeyboardButton("🦎 Рептилії", callback_data='animals_reptiles')
animals_farm_animals = types.InlineKeyboardButton("🐄 Сільгосп тварини", callback_data='animals_farm_animals')
animals_other_animals = types.InlineKeyboardButton("🐾 Інші тварини", callback_data='animals_other_animals')
animals_pet_supplies = types.InlineKeyboardButton("🏬 Зоотовари", callback_data='animals_pet_supplies')
animals_mating = types.InlineKeyboardButton("💑 В'язка", callback_data='animals_mating')
animals_found_bureau = types.InlineKeyboardButton("🔍 Бюро знахідок", callback_data='animals_found_bureau')

animals_markup = types.InlineKeyboardMarkup(row_width=2)
animals_markup.add(animals_dogs, animals_cats, animals_aquarium, animals_birds,
                   animals_rodents, animals_reptiles, animals_farm_animals,
                   animals_other_animals, animals_pet_supplies, animals_mating, animals_found_bureau, go_back)

# house_garden
house_garden_stationery_consumables = types.InlineKeyboardButton("📝 Канцтовари / Витратні матеріали", callback_data='house_garden_stationery_consumables')
house_garden_furniture = types.InlineKeyboardButton("🛋️ Меблі", callback_data='house_garden_furniture')
house_garden_food_drinks = types.InlineKeyboardButton("🍲 Продукти харчування / Напої", callback_data='house_garden_food_drinks')
house_garden_garden = types.InlineKeyboardButton("🌳 Сад / Город", callback_data='house_garden_garden')
house_garden_interior_items = types.InlineKeyboardButton("🖼️ Предмети інтер'єру", callback_data='house_garden_interior_items')
house_garden_construction_repair = types.InlineKeyboardButton("🛠️ Будівництво / Ремонт", callback_data='house_garden_construction_repair')
house_garden_tools = types.InlineKeyboardButton("🔧 Інструменти", callback_data='house_garden_tools')
house_garden_indoor_plants = types.InlineKeyboardButton("🪴 Кімнатні рослини", callback_data='house_garden_indoor_plants')
house_garden_tableware_kitchenware = types.InlineKeyboardButton("🍽️ Посуд / Кухонне приладдя", callback_data='house_garden_tableware_kitchenware')
house_garden_garden_inventory = types.InlineKeyboardButton("🚜 Садовий інвентар", callback_data='house_garden_garden_inventory')
house_garden_household_inventory_chemicals = types.InlineKeyboardButton("🧽 Господарський інвентар / Побутова хімія", callback_data='house_garden_household_inventory_chemicals')
house_garden_other_home_goods = types.InlineKeyboardButton("🏠 Інші товари для дому", callback_data='house_garden_other_home_goods')

house_garden_markup = types.InlineKeyboardMarkup(row_width=2)
house_garden_markup.add(house_garden_stationery_consumables, house_garden_furniture, house_garden_food_drinks,
                        house_garden_garden, house_garden_interior_items, house_garden_construction_repair,
                        house_garden_tools, house_garden_indoor_plants, house_garden_tableware_kitchenware,
                        house_garden_garden_inventory, house_garden_household_inventory_chemicals,
                        house_garden_other_home_goods, go_back)

# electronics
electronics_phones_accessories = types.InlineKeyboardButton("📱 Телефони та аксесуари", callback_data='electronics_phones_accessories')
electronics_computers_components = types.InlineKeyboardButton("💻 Комп'ютери та комплектуючі", callback_data='electronics_computers_components')
electronics_photo_video = types.InlineKeyboardButton("📷 Фото / Відео", callback_data='electronics_photo_video')
electronics_tv_video_equipment = types.InlineKeyboardButton("📺 ТВ / Відеотехніка", callback_data='electronics_tv_video_equipment')
electronics_audio_equipment = types.InlineKeyboardButton("🔊 Аудіотехніка", callback_data='electronics_audio_equipment')
electronics_games_consoles = types.InlineKeyboardButton("🎮 Ігри та ігрові приставки", callback_data='electronics_games_consoles')
electronics_tablets_accessories = types.InlineKeyboardButton("📟 Планшети та аксесуари", callback_data='electronics_tablets_accessories')
electronics_laptops_accessories = types.InlineKeyboardButton("💻 Ноутбуки та аксесуари", callback_data='electronics_laptops_accessories')
electronics_home_appliances = types.InlineKeyboardButton("🏠 Техніка для дому", callback_data='electronics_home_appliances')
electronics_kitchen_appliances = types.InlineKeyboardButton("🍳 Техніка для кухні", callback_data='electronics_kitchen_appliances')
electronics_climate_equipment = types.InlineKeyboardButton("❄️ Кліматичне обладнання", callback_data='electronics_climate_equipment')
electronics_personal_care = types.InlineKeyboardButton("🧴 Індивідуальний догляд", callback_data='electronics_personal_care')
electronics_accessories_components = types.InlineKeyboardButton("🔌 Аксесуари й комплектуючі", callback_data='electronics_accessories_components')
electronics_other_electronics = types.InlineKeyboardButton("🔧 Інша електротехніка", callback_data='electronics_other_electronics')

electronics_markup = types.InlineKeyboardMarkup(row_width=2)
electronics_markup.add(electronics_phones_accessories, electronics_computers_components, electronics_photo_video,
                       electronics_tv_video_equipment, electronics_audio_equipment, electronics_games_consoles,
                       electronics_tablets_accessories, electronics_laptops_accessories, electronics_home_appliances,
                       electronics_kitchen_appliances, electronics_climate_equipment, electronics_personal_care,
                       electronics_accessories_components, electronics_other_electronics, go_back)

# business_services
business_services_auto_moto = types.InlineKeyboardButton("🚗 Авто / Мото послуги", callback_data='business_services_auto_moto')
business_services_beauty_health = types.InlineKeyboardButton("💇 Краса / Здоров'я", callback_data='business_services_beauty_health')
business_services_child_elderly_care = types.InlineKeyboardButton("👶 Догляд за дітьми та літніми людьми", callback_data='business_services_child_elderly_care')
business_services_household = types.InlineKeyboardButton("🏠 Побутові послуги", callback_data='business_services_household')
business_services_cleaning = types.InlineKeyboardButton("🧹 Клінінг", callback_data='business_services_cleaning')
business_services_education_sports = types.InlineKeyboardButton("📚 Послуги освіти та спорту", callback_data='business_services_education_sports')
business_services_transportation = types.InlineKeyboardButton("🚚 Перевезення", callback_data='business_services_transportation')
business_services_specialized_services = types.InlineKeyboardButton("🛠️ Послуги спецтехніки", callback_data='business_services_specialized_services')
business_services_photo_video = types.InlineKeyboardButton("📸 Фото та відеозйомка", callback_data='business_services_photo_video')
business_services_event_organization = types.InlineKeyboardButton("🎉 Організація свят", callback_data='business_services_event_organization')
business_services_appliance_repair = types.InlineKeyboardButton("🛠️ Ремонт та обслуговування техніки", callback_data='business_services_appliance_repair')
business_services_construction_repair = types.InlineKeyboardButton("🔨 Будівництво та ремонт", callback_data='business_services_construction_repair')
business_services_raw_materials_materials = types.InlineKeyboardButton("📦 Сированина / Матеріали", callback_data='business_services_raw_materials_materials')
business_services_secondhand_reception = types.InlineKeyboardButton("🔄 Прийом вторсировини", callback_data='business_services_secondhand_reception')
business_services_tourism_immigration = types.InlineKeyboardButton("✈️ Туризм / Іміграція", callback_data='business_services_tourism_immigration')
business_services_business = types.InlineKeyboardButton("👔 Ділові послуги", callback_data='business_services_business')
business_services_business_sale = types.InlineKeyboardButton("💼 Продаж бізнесу", callback_data='business_services_business_sale')
business_services_animal_services = types.InlineKeyboardButton("🐾 Послуги для тварин", callback_data='business_services_animal_services')
business_services_funeral_services = types.InlineKeyboardButton("⚰️ Ритуальні послуги", callback_data='business_services_funeral_services')
business_services_other_services = types.InlineKeyboardButton("🔧 Інші послуги", callback_data='business_services_other_services')

business_services_markup = types.InlineKeyboardMarkup(row_width=2)
business_services_markup.add(business_services_auto_moto, business_services_beauty_health, business_services_child_elderly_care,
                             business_services_household, business_services_cleaning, business_services_education_sports,
                             business_services_transportation, business_services_specialized_services,
                             business_services_photo_video, business_services_event_organization,
                             business_services_appliance_repair, business_services_construction_repair,
                             business_services_raw_materials_materials, business_services_secondhand_reception,
                             business_services_tourism_immigration, business_services_business, business_services_business_sale,
                             business_services_animal_services, business_services_funeral_services, business_services_other_services, go_back)

# rent_hire
rent_hire_transport_equipment = types.InlineKeyboardButton("🚗 Оренда транспорту та спецтехніки", callback_data='rent_hire_transport_equipment')
rent_hire_bike_moto_rental = types.InlineKeyboardButton("🚲 Прокат велосипедів і мото", callback_data='rent_hire_bike_moto_rental')
rent_hire_equipment_rental = types.InlineKeyboardButton("🛠️ Оренда обладнання", callback_data='rent_hire_equipment_rental')
rent_hire_tool_rental = types.InlineKeyboardButton("🔧 Прокат інструментів", callback_data='rent_hire_tool_rental')
rent_hire_medical_goods_rental = types.InlineKeyboardButton("🏥 Прокат товарів мед призначення", callback_data='rent_hire_medical_goods_rental')
rent_hire_tech_electronics_rental = types.InlineKeyboardButton("🔌 Прокат техніки та електроніки", callback_data='rent_hire_tech_electronics_rental')
rent_hire_event_goods_rental = types.InlineKeyboardButton("🎉 Прокат товарів та заходів", callback_data='rent_hire_event_goods_rental')
rent_hire_sports_tourism_rental = types.InlineKeyboardButton("⚽ Прокат спорт і туристичних товарів", callback_data='rent_hire_sports_tourism_rental')
rent_hire_clothing_accessories_rental = types.InlineKeyboardButton("👗 Прокат одягу та аксесуарів", callback_data='rent_hire_clothing_accessories_rental')
rent_hire_childrens_clothing_rental = types.InlineKeyboardButton("👶 Прокат дитячого одягу та товарів", callback_data='rent_hire_childrens_clothing_rental')
rent_hire_other_goods_rental = types.InlineKeyboardButton("🔄 Інші товари на прокат", callback_data='rent_hire_other_goods_rental')

rent_hire_markup = types.InlineKeyboardMarkup(row_width=2)
rent_hire_markup.add(rent_hire_transport_equipment, rent_hire_bike_moto_rental, rent_hire_equipment_rental,
                     rent_hire_tool_rental, rent_hire_medical_goods_rental, rent_hire_tech_electronics_rental,
                     rent_hire_event_goods_rental, rent_hire_sports_tourism_rental, rent_hire_clothing_accessories_rental,
                     rent_hire_childrens_clothing_rental, rent_hire_other_goods_rental, go_back)

# fashion_style
fashion_style_womens_clothing = types.InlineKeyboardButton("👗 Жіночий одяг", callback_data='fashion_style_womens_clothing')
fashion_style_womens_shoes = types.InlineKeyboardButton("🥿 Жіноче взуття", callback_data='fashion_style_womens_shoes')
fashion_style_mens_clothing = types.InlineKeyboardButton("👔 Чоловічий одяг", callback_data='fashion_style_mens_clothing')
fashion_style_mens_shoes = types.InlineKeyboardButton("👞 Чоловіче взуття", callback_data='fashion_style_mens_shoes')
fashion_style_womens_underwear_swimwear = types.InlineKeyboardButton("🩲 Жіноча білизна та купальники", callback_data='fashion_style_womens_underwear_swimwear')
fashion_style_mens_underwear_swimwear = types.InlineKeyboardButton("🩲 Чоловіча білизна та плавки", callback_data='fashion_style_mens_underwear_swimwear')
fashion_style_headwear = types.InlineKeyboardButton("👒 Головні убори", callback_data='fashion_style_headwear')
fashion_style_for_wedding = types.InlineKeyboardButton("👰 Для весілля", callback_data='fashion_style_for_wedding')
fashion_style_wristwatches = types.InlineKeyboardButton("⌚ Наручні годинники", callback_data='fashion_style_wristwatches')
fashion_style_accessories = types.InlineKeyboardButton("🕶️ Аксесуари", callback_data='fashion_style_accessories')
fashion_style_maternity_clothing = types.InlineKeyboardButton("🤰 Одяг для вагітних", callback_data='fashion_style_maternity_clothing')
fashion_style_beauty_health = types.InlineKeyboardButton("💄 Краса / здоров'я", callback_data='fashion_style_beauty_health')
fashion_style_gifts = types.InlineKeyboardButton("🎁 Подарунки", callback_data='fashion_style_gifts')
fashion_style_workwear_footwear_accessories = types.InlineKeyboardButton("👷 Спецодяг, спецвзуття та аксесуари", callback_data='fashion_style_workwear_footwear_accessories')
fashion_style_miscellaneous = types.InlineKeyboardButton("👚 Мода різне", callback_data='fashion_style_miscellaneous')

fashion_style_markup = types.InlineKeyboardMarkup(row_width=2)
fashion_style_markup.add(fashion_style_womens_clothing, fashion_style_womens_shoes, fashion_style_mens_clothing,
                        fashion_style_mens_shoes, fashion_style_womens_underwear_swimwear, fashion_style_mens_underwear_swimwear,
                        fashion_style_headwear, fashion_style_for_wedding, fashion_style_wristwatches,
                        fashion_style_accessories, fashion_style_maternity_clothing, fashion_style_beauty_health,
                        fashion_style_gifts, fashion_style_workwear_footwear_accessories, fashion_style_miscellaneous, go_back)

# hobbies_recreation_sports
hobbies_antiques_collectibles = types.InlineKeyboardButton("🏺 Антикваріат / Колекції", callback_data='hobbies_antiques_collectibles')
hobbies_musical_instruments = types.InlineKeyboardButton("🎶 Музичні інструменти", callback_data='hobbies_musical_instruments')
hobbies_sports_recreation = types.InlineKeyboardButton("⚽ Спорт / Відпочинок", callback_data='hobbies_sports_recreation')
hobbies_cycling = types.InlineKeyboardButton("🚴 Вело", callback_data='hobbies_cycling')
hobbies_militaria = types.InlineKeyboardButton("🪖 Мілітарія", callback_data='hobbies_militaria')
hobbies_quadcopters_accessories = types.InlineKeyboardButton("🚁 Квадрокоптери та аксесуари", callback_data='hobbies_quadcopters_accessories')
hobbies_books_magazines = types.InlineKeyboardButton("📚 Книги / Журнали", callback_data='hobbies_books_magazines')
hobbies_cd_dvd_vinyl = types.InlineKeyboardButton("💿 CD / DVD / Платівки", callback_data='hobbies_cd_dvd_vinyl')
hobbies_tickets = types.InlineKeyboardButton("🎫 Квитки", callback_data='hobbies_tickets')
hobbies_travel_companions = types.InlineKeyboardButton("🌍 Пошук попутників", callback_data='hobbies_travel_companions')
hobbies_bands_musicians = types.InlineKeyboardButton("🎤 Пошук гуртів / Музикантів", callback_data='hobbies_bands_musicians')
hobbies_miscellaneous = types.InlineKeyboardButton("🛒 Інше", callback_data='hobbies_miscellaneous')

hobbies_markup = types.InlineKeyboardMarkup(row_width=2)
hobbies_markup.add(hobbies_antiques_collectibles, hobbies_musical_instruments, hobbies_sports_recreation,
                   hobbies_cycling, hobbies_militaria, hobbies_quadcopters_accessories, hobbies_books_magazines,
                   hobbies_cd_dvd_vinyl, hobbies_tickets, hobbies_travel_companions, hobbies_bands_musicians,
                   hobbies_miscellaneous, go_back)


#







