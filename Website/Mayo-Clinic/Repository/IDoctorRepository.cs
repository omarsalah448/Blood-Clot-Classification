using Mayo_Clinic.Models;
using Mayo_Clinic.ViewModels;

namespace Mayo_Clinic.Repository
{
    public interface IDoctorRepository
    {
        List<Doctor> GetAll();
        Doctor GetById(string Id);
        void Insert(Doctor doctor);
        Task Edit(string id, RegisterDoctorViewModel doctor);
        void Delete(string Id);
        List<Patient> GetPatientsByDrID(string Id);
        int GetAgeByBirthDate(DateOnly BirthDate);
        string GetSignedInDoctorID();
        Task<ApplicationUser> GetSignedInDoctor();
        //Doctor GetById(int id);
    }
}
