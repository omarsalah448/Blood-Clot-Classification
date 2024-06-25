using Mayo_Clinic.Models;
using Microsoft.AspNetCore.Mvc;

namespace Mayo_Clinic.Repository
{
    public interface IPatientRepository
    {
        List<Patient> GetAll();
        Patient GetById(int Id);
        void Insert(Patient patient);
        void Edit(Patient patient);
        void Delete(int Id);
    }
}
