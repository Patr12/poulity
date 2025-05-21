from django.db import models

# ==== Wateja ====
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


# ==== Kuku ====
class Chicken(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    tag_number = models.CharField(max_length=20, unique=True)
    breed = models.CharField(max_length=50)
    date_acquired = models.DateField()
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='chickens', blank=True, null=True)

    def __str__(self):
        return f"{self.tag_number} - {self.breed}"


# ==== Utagaji Mayai ====
class EggProduction(models.Model):
    chicken = models.ForeignKey(Chicken, on_delete=models.CASCADE, related_name='egg_productions')
    date_laid = models.DateField()
    number_of_eggs = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.chicken.tag_number} - {self.number_of_eggs} eggs on {self.date_laid}"


# ==== Uatamaji ====
class Incubation(models.Model):
    chicken = models.ForeignKey(Chicken, on_delete=models.CASCADE, related_name='incubations')
    start_date = models.DateField()
    expected_hatch_date = models.DateField()
    is_hatched = models.BooleanField(default=False)

    def __str__(self):
        return f"Incubation: {self.chicken.tag_number} - Start: {self.start_date}"


# ==== Vifaranga ====
class Chick(models.Model):
    incubation = models.ForeignKey(Incubation, on_delete=models.CASCADE, related_name='chicks')
    number_of_chicks = models.PositiveIntegerField()
    hatch_date = models.DateField()

    def __str__(self):
        return f"{self.number_of_chicks} hatched on {self.hatch_date}"


# ==== Oda ====
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    product = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order: {self.product} x {self.quantity} by {self.customer.name}"


# ==== Ripoti ====
class Report(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ==== Kalenda ====
class Calendar(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='events')
    event_name = models.CharField(max_length=200)
    event_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.event_name} for {self.customer.name} on {self.event_date}"


# ==== Ulishaji ====
class Feeding(models.Model):
    chicken = models.ForeignKey(Chicken, on_delete=models.CASCADE, related_name='feedings')
    feed_type = models.CharField(max_length=100)
    quantity = models.FloatField(help_text="Kiasi cha chakula (kg/l)")
    feeding_time = models.DateTimeField()

    def __str__(self):
        return f"{self.chicken.tag_number} fed {self.feed_type} at {self.feeding_time}"


# ==== Matumizi ya Maji ====
class WaterConsumption(models.Model):
    chicken = models.ForeignKey(Chicken, on_delete=models.CASCADE, related_name='water_usages')
    liters = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.chicken.tag_number} used {self.liters} L on {self.date}"


# ==== Vifo vya Kuku ====
class Mortality(models.Model):
    chicken = models.ForeignKey(Chicken, on_delete=models.CASCADE, related_name='mortalities')
    reason = models.CharField(max_length=200)
    count = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.count} deaths of {self.chicken.tag_number} on {self.date}"


# ==== Afya ya Kuku ====
class HealthStatus(models.Model):
    HEALTH_CHOICES = [('Healthy', 'Healthy'), ('Sick', 'Sick'), ('Dead', 'Dead')]
    chicken = models.ForeignKey(Chicken, on_delete=models.CASCADE, related_name='health_checks')
    status = models.CharField(max_length=200, choices=HEALTH_CHOICES)
    count = models.PositiveIntegerField(null=True, blank=True)

    checkup_date = models.DateField()

    def __str__(self):
        return f"{self.chicken.tag_number} status: {self.status} on {self.checkup_date}"

class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class VaccinationRecord(models.Model):
    vaccine_type = models.CharField(max_length=100)
    vaccination_date = models.DateField()
    medication_used = models.CharField(max_length=100)
    recorded_at = models.DateTimeField(auto_now_add=True)

class ChickenEnvironment(models.Model):
    temperature = models.CharField(max_length=20)
    humidity = models.CharField(max_length=20)
    cleanliness = models.CharField(max_length=20)
    stocking_density = models.CharField(max_length=50)
    recorded_at = models.DateTimeField(auto_now_add=True)

class NutritionInformation(models.Model):
    feed_type = models.CharField(max_length=100)
    feeding_schedule = models.CharField(max_length=100)
    food_consumption_kg = models.FloatField()
    water_consumption_ml = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

class HealthReport(models.Model):
    health_checkup = models.TextField()
    vet_report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    


# ==== Mipangilio ya Mfumo ====
class Settings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.key}: {self.value}"
    
    # =calenda

EVENT_TYPES = [
    ('laying', 'Kuku Kutaga'),
    ('brooding', 'Kuatamia'),
    ('hatching', 'Kutotoresha'),
    ('vaccination', 'Chanjo'),
    ('order', 'Oda ya Mteja'),
]

class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.title} on {self.date}"

