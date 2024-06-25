using Mayo_Clinic.Models;
using Mayo_Clinic.ViewModels;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Reflection;
using System.Security.Claims;

namespace Mayo_Clinic.Repository
{
    public class DoctorRepository : IDoctorRepository
    {
        private readonly Entity context;
        private readonly UserManager<ApplicationUser> userManager;
        private readonly IHttpContextAccessor httpContextAccessor;
        public DoctorRepository(Entity _context, IHttpContextAccessor _httpContextAccessor,
            UserManager<ApplicationUser> _userManager)
        {
            context = _context;
            httpContextAccessor = _httpContextAccessor;
            userManager = _userManager;
        }
        public List<Doctor> GetAll()
        {
            return context.Doctors.ToList();
        }
        public Doctor GetById(string Id)
        {
            return context.Doctors.FirstOrDefault(d => d.Id == Id);
        }

        public void Insert(Doctor doctor)
        {
            context.Doctors.Add(doctor);
            context.SaveChanges();
        }
        public async Task Edit(string id, RegisterDoctorViewModel doctor)
        {
            ApplicationUser updatedUser = await userManager.FindByIdAsync(id);
            Doctor updatedDoctor = GetById(id);
            updatedUser.FirstName = doctor.FirstName;
            updatedUser.LastName = doctor.LastName;
            updatedUser.Email = doctor.Email;
            updatedUser.PhoneNumber = doctor.PhoneNumber;
            updatedUser.PasswordHash = doctor.Password;
            updatedDoctor.University = doctor.University;
            updatedDoctor.Description = doctor.Description;
            updatedDoctor.Image = doctor.Image;

            await context.SaveChangesAsync(); // Save changes asynchronously
        }
        public void Delete(string Id)
        {
            context.Doctors.Remove(GetById(Id));
            context.SaveChanges();
        }

        public List<Patient> GetPatientsByDrID(string Id)
        {
            return context.Patients.Where(p => p.Docotor_Id == Id).ToList();
        }

        public int GetAgeByBirthDate(DateOnly BirthDate)
        {
            var today = DateTime.Today;
            int Age = today.Year - BirthDate.Year;
            //if (today < BirthDate.AddYears(Age))
            //    Age--; // Adjust age if birthday hasn't occurred yet this year
            return Age;
        }
        public string GetSignedInDoctorID()
        {
            return httpContextAccessor.HttpContext?.User.Claims.FirstOrDefault(c => c.Type == ClaimTypes.NameIdentifier).Value;
        }
        public async Task<ApplicationUser> GetSignedInDoctor()
        {
            var Id = GetSignedInDoctorID();
            return await userManager.FindByIdAsync(Id);
        }
    }
}
