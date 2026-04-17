from django.shortcuts import render, redirect
from django.http import HttpResponse
from myapp.models import Person


def index(request):
    # ส่วนค้นหาข้อมูล
    search = request.GET.get("search", "")
    if search:
        all_person = Person.objects.filter(name__icontains=search)
    else:
        all_person = Person.objects.all()
    return render(request, "index.html", {"all_person": all_person, "search": search})


def form(request):
    if request.method == "POST":
        # รับข้อมูลจากฟอร์ม
        name = request.POST.get("name")
        age = request.POST.get("age")

        # บันทึกข้อมูลลงฐานข้อมูล
        person = Person.objects.create(
            name=name,
            age=age
        )

        # เปลี่ยนเส้นทางไปหน้าแรก
        return redirect("/")
    else:
        # แสดงฟอร์ม
        return render(request, "form.html")


def edit(request, id):
    # ดึงข้อมูลประชากรตาม id
    person = Person.objects.get(id=id)

    if request.method == "POST":
        # รับข้อมูลที่แก้ไขจากฟอร์ม
        name = request.POST.get("name")
        age = request.POST.get("age")

        # อัปเดตข้อมูลในฐานข้อมูล
        person.name = name
        person.age = age
        person.save()

        # เปลี่ยนเส้นทางไปหน้าแรก
        return redirect("/")
    else:
        # แสดงฟอร์มแก้ไขพร้อมข้อมูลเดิม
        return render(request, "edit.html", {"person": person})


def delete(request, id):
    # ดึงข้อมูลประชากรตาม id แล้วลบ
    person = Person.objects.get(id=id)
    person.delete()

    # เปลี่ยนเส้นทางไปหน้าแรก
    return redirect("/")
