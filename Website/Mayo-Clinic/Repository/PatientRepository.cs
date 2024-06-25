using Mayo_Clinic.Models;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json.Linq;
using System;
using System.Configuration;
using System.Text;
using System.Text.Json;

namespace Mayo_Clinic.Repository
{
    public class PatientRepository : IPatientRepository
    {
        private readonly Entity context;
        public PatientRepository(Entity _context)
        {
            context = _context;
        }
        public List<Patient> GetAll()
        {
            return context.Patients.ToList();
        }
        public Patient GetById(int Id)
        {
            return context.Patients.FirstOrDefault(p => p.Id == Id);
        }
        public void Insert(Patient patient)
        {
            context.Patients.Add(patient);
            context.SaveChanges();
        }
        public void Edit(Patient patient)
        {
            Patient UpdatedPatient = GetById(patient.Id);
            UpdatedPatient.Name = patient.Name;
            UpdatedPatient.PhoneNumber = patient.PhoneNumber;
            UpdatedPatient.BirthDate = patient.BirthDate;
            UpdatedPatient.BloodClotImage = patient.BloodClotImage;
            UpdatedPatient.Classification = patient.Classification;
            context.SaveChanges();
        }
        public void Delete(int Id)
        {
            context.Patients.Remove(GetById(Id));
            context.SaveChanges();
        }
    }
}
